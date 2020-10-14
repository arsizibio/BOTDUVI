class FontTypes:
    class Font:
        def __init__(self):
            self.default_lowercase = 'qwertyuiopasdfghjklzxcvbnm1234567890'
            self.default_uppercase = self.default_lowercase.upper()
            self.lowercase_symbols = self.default_lowercase
            self.uppercase_symbols = self.default_uppercase
        def upper(self, text):
            for i in range(len(self.lowercase_symbols)):
                text = text.replace(self.lowercase_symbols[i], self.uppercase_symbols[i])
            return text
        def lower(self, text):
            for i in range(len(self.lowercase_symbols)):
                text = text.replace(self.uppercase_symbols[i], self.lowercase_symbols[i])
            return text
        def transform(self, text):
            for i in range(len(self.default_lowercase)):
                text = text.replace(self.default_lowercase[i], self.lowercase_symbols[i])
            for i in range(len(self.default_uppercase)):
                text = text.replace(self.default_uppercase[i], self.uppercase_symbols[i])
            return text
        
    class Italic(Font):
        def __init__(self):
            self.default_lowercase = 'qwertyuiopasdfghjklzxcvbnm1234567890'
            self.default_uppercase = self.default_lowercase.upper()
            self.lowercase_symbols = '𝘲𝘸𝘦𝘳𝘵𝘺𝘶𝘪𝘰𝘱𝘢𝘴𝘥𝘧𝘨𝘩𝘫𝘬𝘭𝘻𝘹𝘤𝘷𝘣𝘯𝘮1234567890'
            self.uppercase_symbols = '𝘘𝘞𝘌𝘙𝘛𝘠𝘜𝘐𝘖𝘗𝘈𝘚𝘋𝘍𝘎𝘏𝘑𝘒𝘓𝘡𝘟𝘊𝘝𝘉𝘕𝘔1234567890'

    class Bold(Font):
        def __init__(self):
            self.default_lowercase = 'qwertyuiopasdfghjklzxcvbnm1234567890'
            self.default_uppercase = self.default_lowercase.upper()
            self.lowercase_symbols = '𝐪𝐰𝐞𝐫𝐭𝐲𝐮𝐢𝐨𝐩𝐚𝐬𝐝𝐟𝐠𝐡𝐣𝐤𝐥𝐳𝐱𝐜𝐯𝐛𝐧𝐦𝟏𝟐𝟑𝟒𝟓𝟔𝟕𝟖𝟗𝟎'
            self.uppercase_symbols = '𝐐𝐖𝐄𝐑𝐓𝐘𝐔𝐈𝐎𝐏𝐀𝐒𝐃𝐅𝐆𝐇𝐉𝐊𝐋𝐙𝐗𝐂𝐕𝐁𝐍𝐌𝟏𝟐𝟑𝟒𝟓𝟔𝟕𝟖𝟗𝟎'
    
    class BoldItalic(Font):
        def __init__(self):
            self.default_lowercase = 'qwertyuiopasdfghjklzxcvbnm1234567890'
            self.default_uppercase = self.default_lowercase.upper()
            self.lowercase_symbols = '𝙦𝙬𝙚𝙧𝙩𝙮𝙪𝙞𝙤𝙥𝙖𝙨𝙙𝙛𝙜𝙝𝙟𝙠𝙡𝙯𝙭𝙘𝙫𝙗𝙣𝙢1234567890'
            self.uppercase_symbols = '𝙌𝙒𝙀𝙍𝙏𝙔𝙐𝙄𝙊𝙋𝘼𝙎𝘿𝙁𝙂𝙃𝙅𝙆𝙇𝙕𝙓𝘾𝙑𝘽𝙉𝙈1234567890'

    class Handwritting(Font):
        def __init__(self):
            self.default_lowercase = 'qwertyuiopasdfghjklzxcvbnm1234567890'
            self.default_uppercase = self.default_lowercase.upper()
            self.lowercase_symbols = '𝓆𝓌𝑒𝓇𝓉𝓎𝓊𝒾𝑜𝓅𝒶𝓈𝒹𝒻𝑔𝒽𝒿𝓀𝓁𝓏𝓍𝒸𝓋𝒷𝓃𝓂𝟣𝟤𝟥𝟦𝟧𝟨𝟩𝟪𝟫𝟢'
            self.uppercase_symbols = '𝒬𝒲𝐸𝑅𝒯𝒴𝒰𝐼𝒪𝒫𝒜𝒮𝒟𝐹𝒢𝐻𝒥𝒦𝐿𝒵𝒳𝒞𝒱𝐵𝒩𝑀𝟣𝟤𝟥𝟦𝟧𝟨𝟩𝟪𝟫𝟢'
    
    class HandwrittingBold(Font):
        def __init__(self):
            self.default_lowercase = 'qwertyuiopasdfghjklzxcvbnm1234567890'
            self.default_uppercase = self.default_lowercase.upper()
            self.lowercase_symbols = '𝓺𝔀𝓮𝓻𝓽𝔂𝓾𝓲𝓸𝓹𝓪𝓼𝓭𝓯𝓰𝓱𝓳𝓴𝓵𝔃𝔁𝓬𝓿𝓫𝓷𝓶1234567890'
            self.uppercase_symbols = '𝓠𝓦𝓔𝓡𝓣𝓨𝓤𝓘𝓞𝓟𝓐𝓢𝓓𝓕𝓖𝓗𝓙𝓚𝓛𝓩𝓧𝓒𝓥𝓑𝓝𝓜1234567890'

    class Vaporwave(Font):
        def __init__(self):
            self.default_lowercase = 'qwertyuiopasdfghjklzxcvbnm1234567890'
            self.default_uppercase = self.default_lowercase.upper()
            self.lowercase_symbols = 'ｑｗｅｒｔｙｕｉｏｐａｓｄｆｇｈｊｋｌｚｘｃｖｂｎｍ１２３４５６７８９０'
            self.uppercase_symbols = 'ＱＷＥＲＴＹＵＩＯＰＡＳＤＦＧＨＪＫＬＺＸＣＶＢＮＭ１２３４５６７８９０'



class Text:
    def __init__(self, fontType: FontTypes.Font, text: str):
        self.font = fontType()
        self.text = self.font.transform(text)
    @property
    def uppercase(self):
        return self.font.upper(self.text)
    @property
    def lowercase(self):
        return self.font.lower(self.text)
    @property
    def underlined(self):
        return '̲'.join(list(self.text))
    @property
    def double_underlined(self):
        return '̳'.join(list(self.text))
    @property
    def crossed(self):
        return '̷'.join(list(self.text))
    @property
    def through(self):
        return '̶'.join(list(self.text))
    def set_text(self, new_text):
        self.text = self.font.transform(new_text)

    def __str__(self):
        return self.text
    def __repr__(self):
        return self.text