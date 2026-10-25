class Relation:
    def __init__(self, attributes):
        self.attributes = tuple(attributes)
        self.tuples = set()

    def add_tuple(self, values):
        self.tuples.add(tuple(values))

    def __str__(self):
        return str(self.tuples)


def projection(relation, attributes):
    indexes = [relation.attributes.index(a) for a in attributes]

    result = Relation(attributes)
    result.tuples = {
        tuple(row[i] for i in indexes)
        for row in relation.tuples
    }

    return result


def restriction(relation, attribute, value):
    index = relation.attributes.index(attribute)

    result = Relation(relation.attributes)
    result.tuples = {
        row for row in relation.tuples
        if row[index] == value
    }

    return result


if __name__ == "__main__":
    products = Relation(("id", "name", "price"))

    products.add_tuple((1, "retiisi", 7))
    products.add_tuple((2, "porkkana", 5))
    products.add_tuple((3, "nauris", 4))
    products.add_tuple((4, "lanttu", 8))
    products.add_tuple((5, "selleri", 4))

    print(products)

    print(projection(products, ("name",)))
    print(projection(products, ("price",)))
    print(projection(products, ("name", "price")))

    print(restriction(products, "name", "porkkana"))
    print(restriction(products, "price", 4))

    print(projection(restriction(products, "price", 4), ("name",)))
