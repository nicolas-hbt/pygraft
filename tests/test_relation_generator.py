import pytest
from pygraft.relation_generator import RelationGenerator

class TestRelationGenerator:
    @classmethod
    def setup_class(cls):
        # Common setup for all test methods
        cls.relation_generator = RelationGenerator(
            class_info={},
            num_relations=20,
            relation_specificity=0.6,
            prop_profiled_relations=0.5,
            profile_side="both",
            verbose=False,
            prop_symmetric_relations=0.2,
            prop_inverse_relations=0.1,
            prop_functional_relations=0.3,
            prop_inverse_functional_relations=0.1,
            prop_transitive_relations=0.2,
            prop_subproperties=0.1,
            prop_reflexive_relations=0.1,
            prop_irreflexive_relations=0.1,
            prop_asymmetric_relations=0.1
        )

    def test_init(self):
        assert self.relation_generator.class_info == {}
        assert self.relation_generator.num_relations == 20
        assert self.relation_generator.relation_specificity == 0.6
        assert self.relation_generator.prop_profiled_relations == 0.5
        assert self.relation_generator.profile_side == "both"
        assert self.relation_generator.verbose is False
        assert self.relation_generator.prop_symmetric_relations == 0.2
        assert self.relation_generator.prop_inverse_relations == 0.1
        assert self.relation_generator.prop_functional_relations == 0.3
        assert self.relation_generator.prop_inverse_functional_relations == 0.1
        assert self.relation_generator.prop_transitive_relations == 0.2
        assert self.relation_generator.prop_subproperties == 0.1
        assert self.relation_generator.prop_reflexive_relations == 0.1
        assert self.relation_generator.prop_irreflexive_relations == 0.1
        assert self.relation_generator.prop_asymmetric_relations == 0.1

    def test_assemble_relation_info(self):
        relation_info = self.relation_generator.assemble_relation_info()
        assert "statistics" in relation_info
        assert "relations" in relation_info
        assert "rel2patterns" in relation_info
        assert "pattern2rels" in relation_info

        # Add more specific assertions for the assembled information
        statistics = relation_info["statistics"]
        assert "num_relations" in statistics
        assert "prop_reflexive" in statistics
        assert "prop_irreflexive" in statistics
        assert "prop_functional" in statistics
        assert "prop_inversefunctional" in statistics
        assert "prop_symmetric" in statistics
        assert "prop_asymmetric" in statistics
        assert "prop_transitive" in statistics
        assert "prop_inverseof" in statistics
        assert "prop_subpropertyof" in statistics
        assert "prop_profiled_relations" in statistics
        assert "relation_specificity" in statistics

    def test_generate_relations(self):
        self.relation_generator.generate_relations()

        # Add assertions to check if relations and properties are generated correctly
        assert len(self.relation_generator.relations) == 20

    def test_calculate_relation_specificity(self):
        specificity = self.relation_generator.calculate_relation_specificity()
        assert isinstance(specificity, float)
        # Add more specific assertions for relation specificity calculation

    
    def test_calculate_profile_ratio(self):
        # Test when profile_side is "both"
        ratio_both = self.relation_generator.calculate_profile_ratio()
        assert ratio_both >= 0.0 and ratio_both <= 1.0

        # Test when profile_side is "source"
        self.relation_generator.profile_side = "source"
        ratio_source = self.relation_generator.calculate_profile_ratio()
        assert ratio_source >= 0.0 and ratio_source <= 1.0

        # Test when profile_side is "target"
        self.relation_generator.profile_side = "target"
        ratio_target = self.relation_generator.calculate_profile_ratio()
        assert ratio_target >= 0.0 and ratio_target <= 1.0


if __name__ == "__main__":
    pytest.main()
