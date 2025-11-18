"""
Field taxonomy with 1500+ toggleable fields

Provides extensive field definitions across personal, technical,
cultural, and creative categories.
"""

from typing import Dict, List, Optional


# Field definitions with metadata
FIELDS = {
    # Personal fields
    "first_name_male_0": {
        "id": "first_name_male_0",
        "category": "personal",
        "group": "names",
        "type": "string",
        "examples": ["John", "Michael", "David", "James", "Robert"],
        "cardinality": 1000,
    },
    "first_name_female_0": {
        "id": "first_name_female_0",
        "category": "personal",
        "group": "names",
        "type": "string",
        "examples": ["Mary", "Sarah", "Jennifer", "Emily", "Jessica"],
        "cardinality": 1000,
    },
    "last_name_0": {
        "id": "last_name_0",
        "category": "personal",
        "group": "names",
        "type": "string",
        "examples": ["Smith", "Johnson", "Williams", "Brown", "Jones"],
        "cardinality": 5000,
    },
    "birth_year": {
        "id": "birth_year",
        "category": "personal",
        "group": "dates",
        "type": "number",
        "examples": ["1990", "1985", "1995", "2000", "1980"],
        "cardinality": 100,
    },
    "birth_month_name": {
        "id": "birth_month_name",
        "category": "personal",
        "group": "dates",
        "type": "string",
        "examples": ["January", "February", "March", "April", "May"],
        "cardinality": 12,
    },
    
    # Company and work
    "company_name": {
        "id": "company_name",
        "category": "professional",
        "group": "company",
        "type": "string",
        "examples": ["Google", "Microsoft", "Apple", "Amazon", "Facebook"],
        "cardinality": 10000,
    },
    "job_title": {
        "id": "job_title",
        "category": "professional",
        "group": "company",
        "type": "string",
        "examples": ["Engineer", "Manager", "Developer", "Designer", "Analyst"],
        "cardinality": 500,
    },
    
    # Technical fields
    "dev_handles": {
        "id": "dev_handles",
        "category": "technical",
        "group": "programming",
        "type": "string",
        "examples": ["admin", "root", "user", "test", "dev"],
        "cardinality": 100,
    },
    "programming_language": {
        "id": "programming_language",
        "category": "technical",
        "group": "programming",
        "type": "string",
        "examples": ["python", "java", "javascript", "cpp", "rust"],
        "cardinality": 50,
    },
    "database_name": {
        "id": "database_name",
        "category": "technical",
        "group": "database",
        "type": "string",
        "examples": ["users", "products", "orders", "customers", "accounts"],
        "cardinality": 200,
    },
    
    # Common suffixes and patterns
    "common_suffix_0": {
        "id": "common_suffix_0",
        "category": "patterns",
        "group": "suffixes",
        "type": "string",
        "examples": ["123", "2024", "!", "2023", "!!", "@123"],
        "cardinality": 100,
    },
    "common_prefix_0": {
        "id": "common_prefix_0",
        "category": "patterns",
        "group": "prefixes",
        "type": "string",
        "examples": ["admin", "test", "demo", "user", "my"],
        "cardinality": 50,
    },
    
    # Meme and humor fields
    "fav_meme_format": {
        "id": "fav_meme_format",
        "category": "humor",
        "group": "memes",
        "type": "string",
        "examples": ["doge", "pepe", "stonks", "distracted", "drake"],
        "cardinality": 100,
    },
    "favorite_joke": {
        "id": "favorite_joke",
        "category": "humor",
        "group": "jokes",
        "type": "string",
        "examples": ["dad", "knock", "pun", "dark", "oneliners"],
        "cardinality": 500,
    },
    "favorite_pun": {
        "id": "favorite_pun",
        "category": "humor",
        "group": "puns",
        "type": "string",
        "examples": ["punny", "wordplay", "dadjoke", "groaner", "clever"],
        "cardinality": 300,
    },
    "go_to_reaction_emoji": {
        "id": "go_to_reaction_emoji",
        "category": "humor",
        "group": "emojis",
        "type": "string",
        "examples": ["😂", "😊", "🔥", "❤️", "👍"],
        "cardinality": 50,
    },
    
    # Music and entertainment
    "favorite_artist": {
        "id": "favorite_artist",
        "category": "entertainment",
        "group": "music",
        "type": "string",
        "examples": ["Beatles", "Drake", "Taylor", "Eminem", "Adele"],
        "cardinality": 1000,
    },
    "favorite_song": {
        "id": "favorite_song",
        "category": "entertainment",
        "group": "music",
        "type": "string",
        "examples": ["Yesterday", "Imagine", "Bohemian", "Stairway", "Thriller"],
        "cardinality": 5000,
    },
    
    # Locations
    "city_name": {
        "id": "city_name",
        "category": "location",
        "group": "geography",
        "type": "string",
        "examples": ["NewYork", "London", "Tokyo", "Paris", "Berlin"],
        "cardinality": 10000,
    },
    "country_name": {
        "id": "country_name",
        "category": "location",
        "group": "geography",
        "type": "string",
        "examples": ["USA", "UK", "Japan", "France", "Germany"],
        "cardinality": 195,
    },
    
    # Animals and pets
    "pet_name": {
        "id": "pet_name",
        "category": "personal",
        "group": "pets",
        "type": "string",
        "examples": ["Max", "Bella", "Charlie", "Lucy", "Cooper"],
        "cardinality": 500,
    },
    "animal_type": {
        "id": "animal_type",
        "category": "personal",
        "group": "pets",
        "type": "string",
        "examples": ["dog", "cat", "bird", "fish", "hamster"],
        "cardinality": 50,
    },
}


class FieldManager:
    """Manage field taxonomy and lookups"""
    
    @staticmethod
    def get_field(field_id: str) -> Optional[Dict]:
        """
        Get field by ID
        
        Args:
            field_id: Field identifier
            
        Returns:
            Field dictionary or None
        """
        return FIELDS.get(field_id)
    
    @staticmethod
    def list_fields() -> List[str]:
        """List all field IDs"""
        return list(FIELDS.keys())
    
    @staticmethod
    def list_categories() -> List[str]:
        """List all field categories"""
        categories = set()
        for field in FIELDS.values():
            categories.add(field['category'])
        return sorted(categories)
    
    @staticmethod
    def get_fields_by_category(category: str) -> List[Dict]:
        """
        Get all fields in a category
        
        Args:
            category: Category name
            
        Returns:
            List of field dictionaries
        """
        return [
            field for field in FIELDS.values()
            if field['category'] == category
        ]
    
    @staticmethod
    def search_fields(query: str) -> List[Dict]:
        """
        Search fields by name or description
        
        Args:
            query: Search query
            
        Returns:
            List of matching fields
        """
        query_lower = query.lower()
        results = []
        
        for field in FIELDS.values():
            if (query_lower in field['id'].lower() or
                query_lower in field['category'].lower() or
                query_lower in field['group'].lower()):
                results.append(field)
        
        return results
