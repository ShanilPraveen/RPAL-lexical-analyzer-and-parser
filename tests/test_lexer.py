from Lexer import Lexer

def test_tokenization_sample():
    code = "let x = 10 in x + 5"
    lexer = Lexer(code)
    lexer.tokenize()
    tokens = lexer.tokens

    types = [token.type for token in tokens]
    values = [token.value for token in tokens]

    assert 'let' in types
    assert 'identifier' in types
    assert 'integer' in types
    assert '+' in values
