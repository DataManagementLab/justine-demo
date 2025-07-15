import minidb


class Dataset(minidb.Model):
    name = str
    description = str

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description
        }


class Run(minidb.Model):
    dataset = int
    missing_table_names = int
    missing_column_names = int
    num_iterations = int

    def to_dict(self):
        return {
            "id": self.id,
            "dataset": self.dataset,
            "missingTableNames": self.missing_table_names,
            "missingColumnNames": self.missing_column_names,
            "num_iterations": self.num_iterations
        }


class RunStep(minidb.Model):
    run = int
    iteration = int
    cached_result = str


class Interaction(minidb.Model):
    database = int
    num_interactions = int

    def to_dict(self):
        return {
            "id": self.id,
            "database": self.database,
            "num_interactions": self.num_interactions
        }


if __name__ == "__main__":
    db = minidb.Store("data.sqlite")
    db.register(Dataset)

    d = Dataset(name="SPIDER", description="Tables from Spider Benchmark")
    print(d)
    #d.save(db)

    d2 = Dataset(name="TPC-H", description="TPC-H Benchmark")
    print(d2)
    #d2.save(db)

    #db.commit()

    for d in Dataset.load(db):
        print(d)

    print(Dataset.get(db, id=1))

    db.close()
