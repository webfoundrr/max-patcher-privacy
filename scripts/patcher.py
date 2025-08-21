import os
import glob
import sys

DECOMPILED_DIR = "apk_workdir"
PATCHES_DIR = "patches"

def apply_patches():
    print("Smali patching process...")

    total_patches_applied = 0

    all_smali_files = glob.glob(os.path.join(DECOMPILED_DIR, '**', '*.smali'), recursive=True)

    for smali_fPath in all_smali_files:
        try:
            with open(smali_fPath, 'r', encoding='utf-8') as f:
                target_content = f.read()
        except Exception as e:
            print(f"Warning: Could not read {smali_fPath}: {e}")
            continue

        original_content = target_content

        for snippet_path in glob.glob(os.path.join(os.path.join(PATCHES_DIR, "original"), "*.smali-snippet")):
            snippet_filename = os.path.basename(snippet_path)

            with open(snippet_path, 'r', encoding='utf-8') as f:
                original_block = f.read()

            patched_snippet_path = os.path.join(os.path.join(PATCHES_DIR, "patched"), snippet_filename)
            if not os.path.exists(patched_snippet_path):
                print(f"Warning: Matching patched snippet not found for {snippet_filename}")
                continue

            with open(patched_snippet_path, 'r', encoding='utf-8') as f:
                patched_block = f.read()

            if original_block in target_content:
                print(f"  -> Found match for '{snippet_filename}' in '{os.path.basename(smali_fPath)}'. Applying patch.")
                target_content = target_content.replace(original_block, patched_block)
                total_patches_applied += 1

        if original_content != target_content:
            print(f"Writing changes to {smali_fPath}...")
            try:
                with open(smali_fPath, 'w', encoding='utf-8') as f:
                    f.write(target_content)
            except Exception as e:
                print(f"?? (Could not write to {smali_fPath}: {e})")
                sys.exit(1)


    print(f"\nPatching process finished. Total patches applied: {total_patches_applied}")
    if total_patches_applied == 0:
        print("Warning: No patches were applied. The app might have updated significantly!!!")
        sys.exit(1)
    return None


if __name__ == "__main__":
    apply_patches()