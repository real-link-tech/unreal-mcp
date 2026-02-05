import unreal
import os


def import_ui_texture(file_path: str, destination_path: str) -> dict:
	file_path = file_path.replace("\\", "/").replace("\\", "/")
	if not os.path.isfile(file_path):
		raise FileNotFoundError(f"File not found: {file_path}")
	if not file_path.lower().endswith(".png"):
		raise ValueError("File must be a PNG")
	base_name = os.path.splitext(os.path.basename(file_path))[0]
	destination_path = destination_path.strip("/").replace("\\", "/").replace("\\", "/")
	if not destination_path.startswith("Game"):
		if destination_path.startswith("/Game"):
			destination_path = destination_path[1:].strip("/")
		else:
			destination_path = "Game/" + destination_path.strip("/")
	asset_tools = unreal.AssetToolsHelpers.get_asset_tools()
	task = unreal.AssetImportTask()
	task.set_editor_property("filename", file_path)
	task.set_editor_property("destination_path", "/" + destination_path)
	task.set_editor_property("destination_name", base_name)
	task.set_editor_property("replace_existing", True)
	task.set_editor_property("automated", True)
	task.set_editor_property("save", True)
	asset_tools.import_asset_tasks([task])
	imported_path = "/" + destination_path + "/" + base_name
	texture = unreal.EditorAssetLibrary.load_asset(imported_path)
	if not texture:
		return {"success": False, "error": f"Could not load imported asset: {imported_path}"}
	if not isinstance(texture, unreal.Texture2D):
		return {"success": False, "error": f"Imported asset is not Texture2D: {type(texture)}"}
	try:
		ui_group = unreal.TextureGroup.TEXTUREGROUP_UI
	except Exception:
		ui_group = getattr(unreal.TextureGroup, "TEXTUREGROUP_UI", None)
	if ui_group is not None:
		texture.set_editor_property("lod_group", ui_group)
		unreal.EditorAssetLibrary.save_asset(imported_path)
	return {
		"success": True,
		"asset_path": imported_path,
		"texture_group_set": ui_group is not None,
	}


def main():
	result = import_ui_texture("${file_path}", "${destination_path}")
	import json
	print(json.dumps(result))


if __name__ == "__main__":
	main()
