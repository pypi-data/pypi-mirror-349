# import sys
# from pathlib import Path
# import unittest

# Add parent directory to import path
# sys.path.append(str(Path(__file__).parent.parent))

# from chunker.pre_normalize import pre_normalize


# class TestPreNormalize(unittest.TestCase):
#     
#     def test_empty_string(self):
#         self.assertEqual(pre_normalize(""), "")
#         self.assertEqual(pre_normalize(None), "")
#     
#     def test_control_chars_removal(self):
#         self.assertEqual(pre_normalize("Hello\u0000World"), "HelloWorld")
#         self.assertEqual(pre_normalize("Text\u0007with\u001Fcontrol\u0001chars"), "Textwithcontrolchars")
#     
#     def test_unicode_normalize(self):
#         # Example with combined character (ё)
#         self.assertEqual(pre_normalize("ё"), "ё")
#         
#     def test_whitespace_collapse(self):
#         self.assertEqual(pre_normalize("Hello   World"), "Hello World")
#         self.assertEqual(pre_normalize("  Leading and trailing  "), "Leading and trailing")
#         self.assertEqual(pre_normalize("Multiple    spaces   between    words"), "Multiple spaces between words")


# if __name__ == "__main__":
#     unittest.main() 