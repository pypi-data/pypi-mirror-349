import os
import shutil
import unittest
import fm_image_tagger.tag_edit as Editor

class TestTagEditRemove(unittest.TestCase):

    def setUp(self):
        self.test_dir = "test_tag_edit_dir"
        os.makedirs(self.test_dir, exist_ok=True)
        self.test_file_path = os.path.join(self.test_dir, "test_image.txt")

    def tearDown(self):
        if os.path.exists(self.test_dir):
            shutil.rmtree(self.test_dir)

    def test_remove_multiple_tags(self):
        # Initial tags in the file
        initial_tags = "tag1, tag2, tag3, tag4, tag5"
        with open(self.test_file_path, "w", encoding="utf-8") as f:
            f.write(initial_tags + "\n") # Ensure newline like in actual files

        # Tags to remove
        tags_to_remove = ["tag1", "tag3", "tag5"]

        # Expected tags after removal
        expected_tags = "tag2, tag4"

        # Call the remove function
        Editor.remove(self.test_dir, tags_to_remove)

        # Read the file content after removal
        with open(self.test_file_path, "r", encoding="utf-8") as f:
            content_after_removal = f.read().strip()

        # Assert that the content matches the expected tags
        # Normalizing spaces around commas for robust comparison
        normalized_content = ", ".join([tag.strip() for tag in content_after_removal.split(",")])
        normalized_expected = ", ".join([tag.strip() for tag in expected_tags.split(",")])
        self.assertEqual(normalized_content, normalized_expected)

if __name__ == '__main__':
    unittest.main()
