import re
from typing import Union, List
from datetime import datetime, timedelta
from pydantic import BaseModel, validator
from random import choice

import jinja2
import weasyprint


class Acquirer(BaseModel):
    name: str = "Fulano De Tal"
    taxid: str = "000.000.000-00"

    @validator('taxid')
    def validator_taxid(cls, taxid):
        return re.sub(
            '([0-9]{3})\.?([0-9]{3})\.?([0-9]{3})\-?([0-9]{2})',
            r'\1.\2.\3-\4',
            taxid
        )


class Seller(Acquirer):
    ...


class Item(BaseModel):
    quantity: int
    name: str
    price: float


class DataForm(BaseModel):
    issued_at: Union[datetime, str]
    acquirer: Acquirer
    seller: Seller
    items: List[Item]
    
    def total(self):
        return sum((item.price * item.quantity) for item in self.items)


def main():
    acquirer = Acquirer(name='Sicrano de tal', taxid='00000000000')
    seller = Seller(name="Fulano de tal", taxid="000000000000")
    items = [
        Item(quantity=1, name='aluguel', price=250),
    ]
    dataform = DataForm(
        issued_at=datetime.now() - timedelta(days=4),
        acquirer=acquirer,
        seller=seller,
        items=items
    )

    with open('BaseModel.html', 'r', encoding='utf-8') as template_file:
        rendered_template = jinja2.Template(
            template_file.read()
        ).render(dataform=dataform, format=format)
    
    with open('output.html', 'w') as file:
        file.write(rendered_template)
    
    weasyprint.HTML(string=rendered_template).write_pdf(
        f'{acquirer.name}.pdf',
        stylesheets=[weasyprint.CSS(string='@page { size: A3; margin: 1cm }')]
    )


if __name__ == "__main__":
    main()
