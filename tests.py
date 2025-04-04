import pytest
from model import Question


def test_create_question():
    question = Question(title='q1')
    assert question.id != None

def test_create_multiple_questions():
    question1 = Question(title='q1')
    question2 = Question(title='q2')
    assert question1.id != question2.id

def test_create_question_with_invalid_title():
    with pytest.raises(Exception):
        Question(title='')
    with pytest.raises(Exception):
        Question(title='a'*201)
    with pytest.raises(Exception):
        Question(title='a'*500)

def test_create_question_with_valid_points():
    question = Question(title='q1', points=1)
    assert question.points == 1
    question = Question(title='q1', points=100)
    assert question.points == 100

def test_create_choice():
    question = Question(title='q1')
    
    question.add_choice('a', False)

    choice = question.choices[0]
    assert len(question.choices) == 1
    assert choice.text == 'a'
    assert not choice.is_correct

def test_add_multiple_choices():
    question = Question(title='q1')
    question.add_choice('a')
    question.add_choice('b')
    assert len(question.choices) == 2
    assert question.choices[0].text == 'a'
    assert question.choices[1].text == 'b'

def test_choice_ids_are_sequential():
    question = Question(title='q1')
    choice1 = question.add_choice('a')
    choice2 = question.add_choice('b')
    assert choice2.id == choice1.id + 1

def test_remove_choice_by_id():
    question = Question(title='q1')
    choice = question.add_choice('a')
    question.remove_choice_by_id(choice.id)
    assert len(question.choices) == 0

def test_remove_nonexistent_choice_raises_exception():
    question = Question(title='q1')
    question.add_choice('a')
    with pytest.raises(Exception):
        question.remove_choice_by_id(999)  # ID que não existe

def test_remove_all_choices():
    question = Question(title='q1')
    question.add_choice('a')
    question.add_choice('b')
    question.remove_all_choices()
    assert len(question.choices) == 0

def test_set_correct_choices():
    question = Question(title='q1')
    choice1 = question.add_choice('a')
    choice2 = question.add_choice('b')
    question.set_correct_choices([choice1.id])
    assert choice1.is_correct
    assert not choice2.is_correct

def test_select_correct_choices():
    question = Question(title='q1')  # max_selections=1 por padrão
    choice1 = question.add_choice('correct', True)
    choice2 = question.add_choice('wrong', False)
    selected = question.select_choices([choice1.id])
    assert selected == [choice1.id]

def test_select_too_many_choices_raises_exception():
    question = Question(title='q1', max_selections=1)
    choice1 = question.add_choice('a')
    choice2 = question.add_choice('b')
    with pytest.raises(Exception):
        question.select_choices([choice1.id, choice2.id])

def test_choice_text_validation():
    question = Question(title='q1')
    with pytest.raises(Exception):
        question.add_choice('')  # Texto vazio
    with pytest.raises(Exception):
        question.add_choice('a' * 101)  # Texto muito longo

def test_question_points_validation():
    with pytest.raises(Exception):
        Question(title='q1', points=0)  # Pontos abaixo do mínimo
    with pytest.raises(Exception):
        Question(title='q1', points=101)  # Pontos acima do máximo

@pytest.fixture
def question_with_choices():
    question = Question(title="Questão com choices", max_selections=2)
    question.add_choice("Opção 1", False)
    question.add_choice("Opção 2", True)  # Correta
    question.add_choice("Opção 3", True)  # Correta
    return question

def test_select_correct_choices_with_fixture(question_with_choices):
    correct_ids = [choice.id for choice in question_with_choices.choices if choice.is_correct]
    selected = question_with_choices.select_choices(correct_ids)
    assert selected == correct_ids
    assert len(selected) == 2

def test_remove_choice_with_fixture(question_with_choices):
    initial_count = len(question_with_choices.choices)
    choice_to_remove = question_with_choices.choices[0]
    
    question_with_choices.remove_choice_by_id(choice_to_remove.id)
    
    assert len(question_with_choices.choices) == initial_count - 1
    with pytest.raises(Exception):
        question_with_choices.remove_choice_by_id(choice_to_remove.id)  # Choice já removida