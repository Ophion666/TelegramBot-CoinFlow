from models.category import OperationType
from repositories.category_repository import CategoryRepository
from repositories.transaction_repository import TransactionRepository



def parser(message:str):
    new_message = message.split()
    if new_message[0][0] == "-":
        operation = "expense"
    elif new_message[0][0]=="+": operation = "income"
    else: raise ValueError("Используйте формат: -250 кофе")
    if len(new_message) > 1:
        amount = new_message[0][1:]
        category = new_message[1]
        if new_message[2:]:
            comment = new_message[2:]
        else: comment = ""
    else: raise ValueError("Используйте формат: -250 кофе")

    return operation, float(amount), category, " ".join(comment)

def category_track(db, operation: str, amount: float, category_name: str, comment: str):
    category_repo = CategoryRepository(db)
    transaction_repo = TransactionRepository(db)
    category_type = OperationType(operation)
    name_category = category_repo.get_by_name(name=category_name)
    if not name_category:
        name_category = category_repo.create(name=category_name, operation_type=category_type)
    name_id = name_category.id
    transaction = transaction_repo.create(amount=amount, category_id=name_id, comment=comment)
    return transaction


