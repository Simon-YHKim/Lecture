import unittest
from selfstudy_voice_text import clean,pronunciation,slide_narration


class SelfstudyVoiceTextTests(unittest.TestCase):
    def test_command_letters_and_numbers_are_not_matched_inside_other_tokens(self):
        for typed,description in [('A','Choose a value.'),('FROM','Pick a point away from it.'),
                                  ('0','The other value is 0.5.'),('35','The opposite side is -35.')]:
            with self.subTest(typed=typed):
                lesson={'sections':[{'blocks':[{'type':'steps','items':[{'n':1,'actions':[
                    {'type':typed,'do':{'en':description}}]}]}]}]}
                text=slide_narration({'sourceStep':1,'sourceActions':[1]},lesson,'en')
                self.assertIn('Enter '+typed+'.',text)

    def test_blank_or_wrong_language_concept_notes_are_rejected(self):
        for notes in ['', '—', '<b> </b>', 'English 국문']:
            with self.subTest(notes=notes), self.assertRaises(ValueError):
                slide_narration({'notes':notes},{},'en')

    def test_literals_survive_cleanup(self):
        self.assertEqual(clean('<b>Use</b> `<>`, &lt;ByLayer&gt;, Ø25 and **-0.15**.'),'Use <>, <ByLayer>, Ø25 and -0.15.')
        self.assertEqual(clean('Keep &amp;lt; once.'),'Keep &lt; once.')

    def test_relative_coordinates_and_function_key_keep_their_meaning(self):
        self.assertEqual(pronunciation('@-35,0 @31.11<45','en'),
                         'at sign minus 35 comma 0 at sign 31 point 11 less than sign 45')
        self.assertIn('에프 8을',pronunciation('F8을 누릅니다.','ko'))
        self.assertIn('지름 25',pronunciation('Ø25','ko'))
        self.assertEqual(pronunciation('R5 끝원, M5, H7, %%c','ko'),'반지름 5 끝원, 엠 5, 에이치 7, 퍼센트 두 개, 씨')

    def test_split_slide_speaks_only_its_actions_and_side_cards(self):
        step={'n':1,'title':{'en':'Draw the line'},'actions':[
            {'type':'LINE','do':{'en':'Start LINE.'}},
            {'type':'-35,0','do':{'en':'Set the endpoint.'}}],
            'why':{'en':'This sets the datum.'},'expect':{'en':'One line is visible.'},
            'pitfall':{'en':'Check the endpoint.'}}
        lesson={'sections':[{'blocks':[{'type':'steps','items':[step]}]}]}
        first=slide_narration({'sourceStep':1,'sourceActions':[1]},lesson,'en')
        last=slide_narration({'sourceStep':1,'sourceActions':[2]},lesson,'en')
        self.assertEqual(first.count('LINE'),1)
        self.assertIn('datum',first);self.assertNotIn('endpoint',first)
        self.assertIn('Enter -35,0.',last);self.assertNotIn('datum',last)
        self.assertIn('One line is visible.',last)
        self.assertIn('Check the endpoint.',last)

    def test_missing_translation_fails_instead_of_speaking_korean_in_english(self):
        with self.assertRaises(ValueError):
            slide_narration({'sourceStep':1,'sourceActions':[1]},
                {'sections':[{'blocks':[{'type':'steps','items':[{'n':1,'title':{'ko':'제목'},
                    'actions':[{'do':{'ko':'내용'}}]}]}]}]},'en')

    def test_keypresses_and_dropdown_choices_are_not_command_line_typing(self):
        actions=[{'kind':'key','type':'F8','do':{'en':'Turn ortho on.'}},
                 {'kind':'click','type':{'en':'Visible line'},'do':{'en':'from the layer dropdown.'}},
                 {'kind':'alt','type':'M','do':{'en':'If placement is wrong, correct it.'}}]
        lesson={'sections':[{'blocks':[{'type':'steps','items':[{'n':1,'actions':actions}]}]}]}
        text=slide_narration({'sourceStep':1,'sourceActions':[1,2,3]},lesson,'en')
        self.assertIn('Press F8.',text);self.assertNotIn('Enter F8',text)
        self.assertIn('Select Visible line from the layer dropdown.',text)
        self.assertIn('optional command is M',text);self.assertNotIn('Enter M',text)


if __name__=='__main__':unittest.main()
