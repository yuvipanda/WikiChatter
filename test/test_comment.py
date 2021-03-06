import unittest
import wikichatter.comment as comment
import wikichatter.textblock as textblock

LEVEL0 = ""
LEVEL1 = ":"
LEVEL2 = "::"
LEVEL3 = ":::"
LEVEL4 = "::::"
SIGNATURE = "[[User:Name|Name]] ([[User talk:Name|talk]]) 19:40, 18 September 2013 (UTC)"
FILLER = "Text"
EL = "\n"


class CommentTest(unittest.TestCase):

    def test_basic_linear_identification(self):
        text = (
            LEVEL0 + FILLER + EL +
            LEVEL1 + FILLER + SIGNATURE + EL +
            LEVEL0 + FILLER + SIGNATURE + EL
        )
        blocks = textblock.generate_textblock_list(text)

        comments = comment.identify_comments_linear_merge(blocks)

        self.assertEqual(len(comments), 2)

    def test_linear_identification_hierarchy(self):
        text = (
            LEVEL0 + FILLER + EL +
            LEVEL0 + FILLER + SIGNATURE + EL +
            LEVEL1 + FILLER + SIGNATURE + EL +
            LEVEL2 + FILLER + EL +
            LEVEL2 + FILLER + SIGNATURE + EL +
            LEVEL1 + FILLER + SIGNATURE + EL
        )
        blocks = textblock.generate_textblock_list(text)

        comments = comment.identify_comments_linear_merge(blocks)

        self.assertEqual(len(comments), 1)
        self.assertEqual(len(comments[0].comments), 2)
        self.assertEqual(len(comments[0].comments[0].comments), 1)
        self.assertEqual(len(comments[0].comments[1].comments), 0)
