import re
import unicodedata
import numpy as np
from emot.emo_unicode import UNICODE_EMOJI
from emot.emo_unicode import EMOTICONS_EMO
from camel_tools.utils.charmap import CharMapper


class Preprocess:

    def remove_emojis(self, data):
        emoj = re.compile("["
            u"\U0001F600-\U0001F64F"  # emoticons
            u"\U0001F300-\U0001F5FF"  # symbols & pictographs
            u"\U0001F680-\U0001F6FF"  # transport & map symbols
            u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
            u"\U00002500-\U00002BEF"  # chinese char
            u"\U00002702-\U000027B0"
            u"\U00002702-\U000027B0"
            u"\U000024C2-\U0001F251"
            u"\U0001f926-\U0001f937"
            u"\U00010000-\U0010ffff"
            u"\u2640-\u2642" 
            u"\u2600-\u2B55"
            u"\u200d"
            u"\u23cf"
            u"\u23e9"
            u"\u231a"
            u"\ufe0f"  # dingbats
            u"\u3030"
                        "]+", re.UNICODE)
        return re.sub(emoj, '', data)
    
    def strip_accents(self, text):
        """
        Strip accents from input String.

        :param text: The input string.
        :type text: String.

        :returns: The processed String.
        :rtype: String.
        """
        try:
            text = unicode(text, 'utf-8')
        except (TypeError, NameError): # unicode is a default on python 3 
            pass
        text = unicodedata.normalize('NFD', text)
        text = text.encode('ascii', 'ignore')
        text = text.decode("utf-8")
        return str(text)

    def text_to_id(self, text):
        """
        Convert input text to id.

        :param text: The input string.
        :type text: String.

        :returns: The processed String.
        :rtype: String.
        """
        text = self.strip_accents(text.lower())
        text = re.sub('[^0-9a-zA-Z_-]', ' ', text)
        return text

    def clean_text(self, text):
        #Remove punctuations
        text = re.sub(r'[?!.;:,#@-]', '', text)

        #Convert to lowercase to maintain consistency
        text = text.lower()
        text = text.strip()
        return text
    
    def respell(self, s):
        respellings = {
                    '|': 'A', 
                    "'": '', 
                    'p':'a', 
                    "Y":'a', 
                    '<':'I', 
                    '$':'sh', 
                    '>': 'A', 
                    '*':'d', 
                    '~':"", 
                    '}':"", 
                    '&':'a',
                    'Z':'T'
                    }
        for wrong in respellings:
            try:
                index = s.index(wrong)
                s = s[:index] + respellings[wrong] + s[len(wrong)+index:]
            except:
                pass
        return ''.join(s)

    def arabic_translation(self, names_df, ar2bw = CharMapper.builtin_mapper('ar2bw')):
        names_df['name'] =[ar2bw(text) for text in names_df['name']]
        names_df['name']=[self.respell(name) for name in  names_df['name']]
        names_df['name'] = names_df['name'].apply(lambda x: x.lower())
        return names_df
    
    def Encode(self, names_df):

        # Step 1: Pad names with matrix to make all names same dimension
        name_length = 20
        nb_char=27
        names_df['encoded_name']=[np.zeros((name_length,nb_char)) for name in names_df['name']]

        # Step 2: Encode Characters to Numbers
        names_df['alpha_name'] = [
            [
                int(max(0.0, ord(char)-96.0))
                for char in name
            ]
            for name in names_df['name']
        ]

        # Step 3: Encode names to matrix of 0 and 1
        for num in range(len(names_df)):
            for i, j in zip(range(len(names_df['alpha_name'][num])), names_df['alpha_name'][num]):
                names_df['encoded_name'][num][i,j]=1

        return names_df.drop('alpha_name', axis=1)
    
    def preprocess(self, names_df, train=True):
        #Step 1 : Drop duplicates and NaN, fixe genders
        names_df.dropna(subset='name',inplace=True)
        try:
            names_df.gender.fillna('/', inplace=True)
        except:
            pass
        #Step 2 : cleaning names
        names_df['name'] = names_df.name.apply(lambda x: self.remove_emojis(x))
        names_df['name']= names_df.name.apply(lambda x: self.text_to_id(x))
        names_df['name'] = names_df.name.apply(lambda x: self.clean_text(x))
        names_df=names_df.dropna(subset='name').reset_index(drop=True)
        #Step 3 : drop short names
        index=[]
        for i in range(len(names_df)):
            if len(names_df.name[i])<3:
                index.append(i)
        names_df=names_df.drop(index)
        names_df=names_df.reset_index(drop=True)

        #Step 1: standardize names
        names_df=self.arabic_translation(names_df)
        names_df=self.Encode(names_df)
        return names_df