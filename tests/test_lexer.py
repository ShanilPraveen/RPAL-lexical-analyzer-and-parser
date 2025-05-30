from Lexer import Lexer

def test_lexer_tokens_simple():
    code = "let x = 10 in x + 1"
    lexer = Lexer(code)
    lexer.tokenize()
    token_values = [t.value for t in lexer.tokens]
    assert "let" in token_values
    assert "x" in token_values
    assert "=" in token_values
