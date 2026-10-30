import os, requests
from urllib.parse import quote
from classifier import groq_folder_match

GRAPH_ENDPOINT = "https://graph.microsoft.com/v1.0"

RULES = {
    ".pdf": "Documents",
    ".docx": "Documents",
    ".xlsx": "Spreadsheets",
    ".png": "Images",
    ".jpg": "Images",
    ".zip": "Archives",
}

def pick_folder(fileName: str) -> str | None:
    ext = os.path.splitext(fileName)[1].lower() # e.g. Report.PDF -> .pdf
    return RULES.get(ext)

def get_headers(accessToken: str) -> dict:
    return {
        "Authorization": f"Bearer {accessToken}",
        "Content-Type": "application/json"
    }

def get_root_files(accessToken: str) -> list[dict]:

    url = f"{GRAPH_ENDPOINT}/me/drive/root/children"
    headers = get_headers(accessToken)

    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        data = response.json()

        files = []
        for item in data.get("value", []):
            if "folder" not in item:
                files.append({
                    "id": item.get("id"),
                    "name": item.get("name"),
                    "mimeType": item.get("file", {}).get("mimeType", "")
                })
        return files

    except requests.exceptions.RequestException as e:
        print("[One Drive Graph] failed: ", e)
        return []

def get_root_folders(accessToken: str) -> dict[str, str]:
    url = f"{GRAPH_ENDPOINT}/me/drive/root/children?$top=200"
    try:
        r = requests.get(url, headers=get_headers(accessToken), timeout=10)
        r.raise_for_status()

        return {i["name"]: i["id"] for i in r.json().get("value", []) if "folder" in i}

    except requests.exceptions.RequestException as e:
        print("[Graph] get_root_folders failed:", e)
        return {}

def folder_id(accessToken: str, folderName: str) -> str | None:
    headers = get_headers(accessToken)

    try:
        r = requests.get(f"{GRAPH_ENDPOINT}/me/drive/root:/{quote(folderName)}",
                         headers=headers, timeout=10)

        if r.status_code == 200:
            return r.json().get("id")
        if r.status_code != 404:
            print("[Graph] folder lookup failed", r.status_code, r.text)
            return None

        payload = {
            "name": folderName,
            "folder": {},                                    # an empty 'folder' object means "make a folder"
            "@microsoft.graph.conflictBehavior": "fail"      # error instead of overwriting if it appears meanwhile
        }
        c = requests.post(f"{GRAPH_ENDPOINT}/me/drive/root/children?$top=200",
                          headers=headers, json=payload, timeout=10)
        c.raise_for_status()
        return c.json().get("id")

    except requests.exceptions.RequestException as e:
        print("[Graph] failed:", e)
        return None

def move_file(accessToken: str, itemId: str, folderId: str) -> bool:
    url = f"{GRAPH_ENDPOINT}/me/drive/items/{itemId}"
    body = {"parentReference": {"id": folderId}}   # PATCH = "change only these fields"; the new parent = a move
    try:
        r = requests.patch(url, headers=get_headers(accessToken), json=body, timeout=10)
        r.raise_for_status()
        return True
    except requests.exceptions.RequestException as e:
        print("[Graph] move failed:", e, getattr(e.response, "text", ""))
        return False

def organise_root(accessToken: str) -> list[str]:
    messages = []
    folders = get_root_folders(accessToken)

    
    files = get_root_files(accessToken)
    matches = groq_folder_match([f["name"] for f in files], list(folders))

    if matches is None:
        return ["Groq unavailable"]

    for f in files:
        name = f["name"]
        target = matches.get(name) 

        if not target:
            target = pick_folder(name)
            if not target:
                continue
            if target not in folders:
                folders[target] = folder_id(accessToken, target)

        folderId = folders.get(target)
        if not folderId:
            messages.append(f"Could not get folder {target}")
        elif move_file(accessToken, f["id"], folderId):
            messages.append(f"Moved {name} -> {target}")
        else:
            messages.append(f"Failed to move {name}")

    return messages or ["Nothing to organise"]