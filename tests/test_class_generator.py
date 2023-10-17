import pytest

from pygraft.class_generator import ClassGenerator

class TestClassGenerator:
    @classmethod
    def setup_class(cls):
        # Common setup for all test methods
        cls.generator = ClassGenerator(
            num_classes=20,
            max_hierarchy_depth=5,
            avg_class_depth=2.5,
            class_inheritance_ratio=0.6,
            avg_disjointness=0.2,
            verbose=False,
        )

    def test_generate_classes(self):
        self.generator.generate_classes()
        assert len(self.generator.classes) == 20
        assert all(isinstance(class_name, str) for class_name in self.generator.classes)

    def test_link_child2parent(self):
        self.generator.link_child2parent("Child1", "Parent", layer=2)
        assert self.generator.class2subclasses_direct.get("Parent") == ["Child1"]
        assert self.generator.class2superclass_direct.get("Child1") == "Parent"
        assert "Child1" in self.generator.layer2classes[2]

    def test_generate_class_hierarchy(self):
        self.generator.generate_class_hierarchy()
        assert len(self.generator.layer2classes) <= 5  # Max hierarchy depth
        assert len(self.generator.classes) == 20  # Number of classes

    def test_generate_class_disjointness(self):
        self.generator.generate_class_disjointness()
        assert len(self.generator.disjointwith) > 0
        assert len(self.generator.mutual_disjointness) > 0

    def test_generate_class_schema(self):
        class_info = self.generator.generate_class_schema()
        assert "num_classes" in class_info
        assert "classes" in class_info
        assert "hierarchy_depth" in class_info
        assert "avg_class_depth" in class_info
        assert "class_inheritance_ratio" in class_info
        assert "direct_class2subclasses" in class_info
        assert "direct_class2superclass" in class_info
        assert "transitive_class2subclasses" in class_info
        assert "transitive_class2superclasses" in class_info
        assert "avg_class_disjointness" in class_info
        assert "class2disjoints" in class_info
        assert "class2disjoints_symmetric" in class_info
        assert "class2disjoints_extended" in class_info
        assert "layer2classes" in class_info
        assert "class2layer" in class_info

    def test_assemble_class_info(self):
        class_info = self.generator.assemble_class_info()
        assert "num_classes" in class_info
        assert "classes" in class_info
        assert "hierarchy_depth" in class_info
        assert "avg_class_depth" in class_info
        assert "class_inheritance_ratio" in class_info
        assert "direct_class2subclasses" in class_info
        assert "direct_class2superclass" in class_info
        assert "transitive_class2subclasses" in class_info
        assert "transitive_class2superclasses" in class_info
        assert "avg_class_disjointness" in class_info
        assert "class2disjoints" in class_info
        assert "class2disjoints_symmetric" in class_info
        assert "class2disjoints_extended" in class_info
        assert "layer2classes" in class_info
        assert "class2layer" in class_info

if __name__ == "__main__":
    pytest.main()
