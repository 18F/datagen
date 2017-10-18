from pytest import raises

from datagen import main


def test_demands_required_arguments():
    with raises(SystemExit):
        main([])


def _run_main(tmpdir, schema, args):
    test_tmpdir = tmpdir.mkdir("testdata")
    schemafile = test_tmpdir.join("schema.txt")
    schemafile.write(schema)
    outfile = test_tmpdir.join("result.txt")
    args += ['-s', schemafile.strpath, outfile.strpath]
    main(args)
    with open(outfile.strpath) as outfile_obj:
        result = outfile_obj.read()
    return result


SCHEMA_FROM_README = """
	#name      type[argument]
	id         int[6]
	first      firstname
	last       lastname
	email      email
	dob        date[after=1945-01-01, before=2001-01-01]
	password   string[8]
	is_active  bool
	language   randomset[python,ruby,go,java,c,js,brainfuck]
    """


def test_as_in_readme(tmpdir):
    # import pytest; pytest.set_trace()
    args = ['-n', '5', '--with-header']
    result = _run_main(tmpdir, SCHEMA_FROM_README, args)
    assert result.count('|') == 42


def test_without_headers(tmpdir):
    args = ['-n', '5']
    result = _run_main(tmpdir, SCHEMA_FROM_README, args)
    assert result.count('|') == 35


def test_delimiter(tmpdir):
    args = ['-n', '5', '--with-header', '-d', ',']
    result = _run_main(tmpdir, SCHEMA_FROM_README, args)
    assert result.count(',') == 42
    assert result.count('|') == 0

def test_lorem_sentence(tmpdir):
    args = ['-n', '1']
    schema = "blather   lorem"
    result = _run_main(tmpdir, schema, args)
    n_words = len(result.split())
    assert n_words > 2
    n_paragraph_breaks = result.count('\n\n')
    assert n_paragraph_breaks == 0
    avg_word_len = len(result) / len(result.splitlines())
    assert avg_word_len > 2

def test_lorem_paragraph(tmpdir):
    args = ['-n', '1']
    schema = "blather   lorem-paragraph"
    result = _run_main(tmpdir, schema, args)
    n_words = len(result.split())
    assert n_words > 6
    n_paragraph_breaks = result.count('\n\n')
    assert n_paragraph_breaks == 0
    avg_word_len = len(result) / len(result.splitlines())
    assert avg_word_len > 2

def test_lorem_long(tmpdir):
    args = ['-n', '1']
    schema = "blather   lorem-long"
    result = _run_main(tmpdir, schema, args)
    n_words = len(result.split())
    assert n_words > 10
    n_lines = len(result.splitlines())
    assert n_lines > 1
    n_paragraph_breaks = result.count('\n\n')
    assert n_paragraph_breaks > 0
    avg_word_len = len(result) / len(result.splitlines())
    assert avg_word_len > 2

def test_word(tmpdir):
    args = ['-n', '10']
    schema = "word   word"
    result = _run_main(tmpdir, schema, args)
    n_words = len(result.split())
    assert n_words == 10
    avg_word_len = len(result) / len(result.splitlines())
    assert avg_word_len > 2


def test_words_unspecified_number(tmpdir):
    args = ['-n', '10']
    schema = "words   words"
    result = _run_main(tmpdir, schema, args)
    n_words = len(result.split())
    assert 20 <= n_words <= 50
    avg_word_len = len(result) / len(result.splitlines())
    assert avg_word_len > 2


def test_words_specified_number(tmpdir):
    args = ['-n', '10']
    schema = "words   words[3]"
    result = _run_main(tmpdir, schema, args)
    n_words = len(result.split())
    assert n_words == 30

def test_words_specified_range(tmpdir):
    args = ['-n', '5']
    schema = "words   words[5,10]"
    result = _run_main(tmpdir, schema, args)
    n_words = len(result.split())
    assert 25 <= n_words <= 50