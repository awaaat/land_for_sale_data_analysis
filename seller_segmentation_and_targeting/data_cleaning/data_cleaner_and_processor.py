import logging
import logging.handlers
import os
import pandas as pd
import re
import numpy as np
from utilities import Utilities

logger = logging.getLogger(__name__)
LOG_LEVEL = "DEBUG"
LOG_FILE = "data_cleaning.log"

# Ensure the log file directory exists
log_dir = os.path.dirname(LOG_FILE)
if log_dir and not os.path.exists(log_dir):
    os.makedirs(log_dir)

# Set log level
logger.setLevel(getattr(logging, LOG_LEVEL))

# Custom formatter with detailed information
formatter = logging.Formatter(
    '%(asctime)s - %(name)s - %(levelname)s - cleaner_and_processor.py : %(lineno)d-%(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

# Console handler
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.DEBUG)
console_handler.setFormatter(formatter)

# Rotating file handler (size-based rotation, max 5MB per file, keep 5 backups)
file_handler = logging.handlers.RotatingFileHandler(
    LOG_FILE,
    maxBytes=5 * 1024 * 1024,  # 5MB
    backupCount=5
)
file_handler.setLevel(logging.DEBUG)
file_handler.setFormatter(formatter)

# Timed rotating file handler (rotates daily, keeps 7 days of logs)
timed_file_handler = logging.handlers.TimedRotatingFileHandler(
    LOG_FILE,
    when='midnight',
    interval=1,
    backupCount=7
)
timed_file_handler.setLevel(logging.DEBUG)
timed_file_handler.setFormatter(formatter)

# Add handlers to the logger
logger.addHandler(console_handler)
logger.addHandler(file_handler)

class DataProcessor:
    
    @staticmethod
    def extract_and_fill_size(df: pd.DataFrame) -> pd.DataFrame:
        """
        Extracts property size information from text fields and populates a new 'size' column in the DataFrame.
        """
        pattern = re.compile(
            r"(?:"  # Non-capturing group for all patterns
            r"(?<!\w)(?:quarter|half|one?|two|three*?|four|for(t(h)?)?|five|fif(t(h)?)?|six(t(h)?)?|seven(t(h)?s?)?|eigh(t(h)?)?|nine(t(h)?)?|ten(t(h)?s?)?|eleven|twelve|thirteen|fourteen|fifteen|twenty|thirty|forty|fifty)(?:th|rd|nd|s)?\s*(?:an\s+)?(?:acre|acres|ac|acr|acrs)(?!\w)|"  # Written numbers
            r"(?<!\w)(?:[Qq]uarter|[Hh]alf|[Oo]ne|[Tt]wo|[Tt]hree|[Ff]our|[Ff]or(t(h)?)?|[Ff]ive|[Ff]if(t(h)?)?|[Ss]ix(t(h)?)?|[Ss]even(t(h)?s?)?|[Ee]igh(t(h)?)?|[Nn]ine(t(h)?)?|[Tt]en(t(h)?s?)?|[Ee]leven|[Tt]welve|[Tt]hirteen|[Ff]ourteen|[Ff]ifteen|[Tt]wenty|[Tt]hirty|[Ff]orty|[Ff]ifty)(?:th|rd|nd|s)?\s*(?:an\s+)?(?:[Aa]cre|[Aa]cres|ac|acr|acrs)(?!\w)|"  # Capitalized written numbers
            r"\b(\d{1,3}(?:,\d{3})*(?:\.\d+)?)\s*(?:acres?|ac|acr|acrs|ha|hectares?)\b|"  # Numeric acres/hectares with commas
            r"\b(\d{1,3}(?:,\d{3})*(?:\.\d+)?)-(?:[Aa]cre|[Aa]cres|ac|acr|acrs|ha|[Hh]ectares?)\b|"  # Hyphenated numeric acres with commas
            r"\b\d+\.?\d*\s*(?:[x*×#/-]|by)\s*\d+\.?\d*\s*(?:ft|feet|fts|m)?\b|"  # Dimensions
            r"\b\d+/\d+\s*th\s*(?:acre|acres|ac|acr|acrs)\b|"  # Fractions with 'th'
            r"\b\d+/\d+\s*(?:acre|acres|ac|acr|acrs)\b|"  # Fractions without 'th'
            r"\b\d+\s*/\s*(?:acre|acres|ac|acr|acrs)\b|"  # Price per acre
            r"\b(?:slightly\s+more\s+than\s+a\s+quarter)\s*(?:acre|acres|ac|acr|acrs)\b|"  # Edge case
            r"\b\d+\s*ft\s*\*\s*\d+\s*ft\b|"  # Specific ft format
            r"\bNumber\s+of\s+plots\s*:\s*\d+\b"  # Number of plots
            r")"
        )
        try:
            search_columns = ['title', 'description', 'property_details']
            def normalize_text(text):
                return str(text).replace('Â', 'A').replace('×', 'x').replace('\n', ' ').strip()
            def extract_match(row):
                combined_text = "  ".join(normalize_text(row[col]) for col in search_columns if normalize_text(row[col]))
                match = pattern.search(combined_text)
                return match[0] if match else np.nan
            df['size'] = df.apply(extract_match, axis=1)
            df.dropna(subset=["size"], inplace=True)
            logger.info("Success. Size fields extracted and filled")
            return df
        
        except Exception as e:
            logger.error("Error while extracting text matches")
            raise e
        
    @staticmethod 
    def convert_to_acreage(df: pd.DataFrame) -> pd.DataFrame:
        """
        Converts the 'size' column in the DataFrame to acres and populates a new 'acreage' column.
        """
        pattern = re.compile(
            r"(?:"  # Non-capturing group for all patterns
            r"(?<!\w)(?:quarter|half|one?|two|three*?|four|for(t(h)?)?|five|fif(t(h)?)?|six(t(h)?)?|seven(t(h)?s?)?|eigh(t(h)?)?|nine(t(h)?)?|ten(t(h)?s?)?|eleven|twelve|thirteen|fourteen|fifteen|twenty|thirty|forty|fifty)(?:th|rd|nd|s)?\s*(?:an\s+)?(?:acre|acres|ac|acr|acrs)(?!\w)|"  # Written numbers
            r"(?<!\w)(?:[Qq]uarter|[Hh]alf|[Oo]ne|[Tt]wo|[Tt]hree|[Ff]our|[Ff]or(t(h)?)?|[Ff]ive|[Ff]if(t(h)?)?|[Ss]ix(t(h)?)?|[Ss]even(t(h)?s?)?|[Ee]igh(t(h)?)?|[Nn]ine(t(h)?)?|[Tt]en(t(h)?s?)?|[Ee]leven|[Tt]welve|[Tt]hirteen|[Ff]ourteen|[Ff]ifteen|[Tt]wenty|[Tt]hirty|[Ff]orty|[Ff]ifty)(?:th|rd|nd|s)?\s*(?:an\s+)?(?:[Aa]cre|[Aa]cres|ac|acr|acrs)(?!\w)|"  # Capitalized written numbers
            r"\b(\d{1,3}(?:,\d{3})*(?:\.\d+)?)\s*(?:acres?|ac|acr|acrs|ha|hectares?)\b|"  # Numeric acres/hectares with commas
            r"\b(\d{1,3}(?:,\d{3})*(?:\.\d+)?)-(?:[Aa]cre|[Aa]cres|ac|acr|acrs|ha|[Hh]ectares?)\b|"  # Hyphenated numeric acres with commas
            r"\b\d+\.?\d*\s*(?:[x*×#/-]|by)\s*\d+\.?\d*\s*(?:ft|feet|fts|m)?\b|"  # Dimensions
            r"\b\d+/\d+\s*th\s*(?:acre|acres|ac|acr|acrs)\b|"  # Fractions with 'th'
            r"\b\d+/\d+\s*(?:acre|acres|ac|acr|acrs)\b|"  # Fractions without 'th'
            r"\b\d+\s*/\s*(?:acre|acres|ac|acr|acrs)\b|"  # Price per acre
            r"\b(?:slightly\s+more\s+than\s+a\s+quarter)\s*(?:acre|acres|ac|acr|acrs)\b|"  # Edge case
            r"\b\d+\s*ft\s*\*\s*\d+\s*ft\b|"  # Specific ft format
            r"\bNumber\s+of\s+plots\s*:\s*\d+\b"  # Number of plots
            r")"
        )

        def parse_written_number(text):
            """Parse written numbers from 1 to 1000."""
            written_numbers = {
                'quarter': 0.25, 'half': 0.5, 'on': 1, 'one': 1.0, 'two': 2.0, 'three': 3.0, 'four': 4.0,
                'five': 5.0, 'six': 6.0, 'seven': 7.0, 'eight': 8.0, 'eighth': 0.125, 'nine': 9.0,
                'ten': 10.0, 'eleven': 11.0, 'twelve': 12.0, 'thirteen': 13.0, 'fourteen': 14.0,
                'fifteen': 15.0, 'sixteen': 16.0, 'seventeen': 17.0, 'eighteen': 18.0, 'nineteen': 19.0,
                'twenty': 20.0, 'thirty': 30.0, 'forty': 40.0, 'fifty': 50.0, 'sixty': 60.0,
                'seventy': 70.0, 'eighty': 80.0, 'ninety': 90.0
            }
            hundreds = {f'{n} hundred': i * 100.0 for i, n in enumerate(['', 'one', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight', 'nine'], start=0)}

            text = text.lower().replace(' an ', ' ').replace(' and ', ' ').strip()
            text = re.sub(r'(?:th|rd|nd|s)?\s*(?:acre|acres|ac|acr|acrs)\b', '', text).strip()

            if text in written_numbers:
                return written_numbers[text]
            if text in hundreds:
                return hundreds[text]

            decimal_match = re.match(r'^\d+\.\d+$', text)
            if decimal_match:
                return float(text)

            parts = text.split()
            total = 0.0
            if len(parts) > 1 and parts[1] == 'hundred':
                hundreds_value = hundreds.get(f'{parts[0]} hundred', 0.0)
                total += hundreds_value
                if len(parts) > 2:
                    remainder = ' '.join(parts[2:])
                    if remainder in written_numbers:
                        total += written_numbers[remainder]
                    else:
                        tens_part = parts[2] if len(parts) > 2 else ''
                        units_part = parts[3] if len(parts) > 3 else ''
                        tens = written_numbers.get(tens_part, 0.0)
                        units = written_numbers.get(units_part, 0.0)
                        total += tens + units
            elif text in [f'{t} {u}' for t in ['twenty', 'thirty', 'forty', 'fifty', 'sixty', 'seventy', 'eighty', 'ninety']
                        for u in ['one', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight', 'nine']]:
                tens, units = text.split()
                total = written_numbers.get(tens, 0.0) + written_numbers.get(units, 0.0)
            
            return float(total) if total > 0 else None

        def map_to_acres(size):
            if pd.isna(size):
                return np.nan
            
            text = str(size).lower().strip()
            match = pattern.search(text)
            if not match:
                return np.nan
            
            matched_text = match.group(0).lower()

            # Fractions (e.g., "1/4 acre", "1/8th ac")
            fraction_match = re.match(r'\b(\d+)/(\d+)\s*(?:th)?\s*(?:acre|acres|ac|acr|acrs)\b', matched_text, re.IGNORECASE)
            if fraction_match:
                num, denom = map(int, fraction_match.groups())
                return float(num) / denom

            # Written numbers, fractions, or decimals
            written_match = re.match(r'(?<!\w)(\d+/\d+|\d+\.\d+|quarter|half|one*?|two|three*?|four|five|six|seven|eigh(?:t|th)|nine|ten|eleven|twelve|thirteen|fourteen|fifteen|sixteen|seventeen|eighteen|nineteen|twenty|thirty|forty|fifty|sixty|seventy|eighty|ninety|(?:one|two|three|four|five|six|seven|eight|nine)\s+hundred(?:\s*(?:twenty|thirty|forty|fifty|sixty|seventy|eighty|ninety)?(?:\s*(?:one|two|three|four|five|six|seven|eight|nine))?)?)(?:th|rd|nd|s)?\s*(?:an\s+)?(?:acre|acres|ac|acr|acrs)(?!\w)', matched_text, re.IGNORECASE)
            if written_match:
                parsed_value = parse_written_number(written_match.group(1))
                if parsed_value is not None:
                    return parsed_value

            fraction = {
                '650 / acre': 650,
                '1/2': 0.5, '1/2acre': 0.5, '1/2 acre': 0.5, '1/2-acre': 0.5, '1/2acres': 0.5, '1/2 acres': 0.5, '1/2-acres': 0.5,
                '1/4': 0.25, '1/4acre': 0.25, '1/4 acre': 0.25, '1/4-acre': 0.25, '1/4acres': 0.25, '1/4 acres': 0.25, '1/4-acres': 0.25,
                '1/8': 0.125, '1/8acre': 0.125, '1/8 acre': 0.125, '1/8-acre': 0.125, '1/8acres': 0.125, '1/8 acres': 0.125, '1/8-acres': 0.125,
                '1/3': 0.3333, '1/3acre': 0.3333, '1/3 acre': 0.3333, '1/3-acre': 0.3333, '1/3acres': 0.3333, '1/3 acres': 0.3333, '1/3-acres': 0.3333,
                '2/3': 0.6667, '2/3acre': 0.6667, '2/3 acre': 0.6667, '2/3-acre': 0.6667, '2/3acres': 0.6667, '2/3 acres': 0.6667, '2/3-acres': 0.6667,
                '3/4': 0.75, '3/4acre': 0.75, '3/4 acre': 0.75, '3/4-acre': 0.75, '3/4acres': 0.75, '3/4 acres': 0.75, '3/4-acres': 0.75,
                '5/8': 0.625, '5/8acre': 0.625, '5/8 acre': 0.625, '5/8-acre': 0.625, '5/8acres': 0.625, '5/8 acres': 0.625, '5/8-acres': 0.625,
                '7/8': 0.875, '7/8acre': 0.875, '7/8 acre': 0.875, '7/8-acre': 0.875, '7/8acres': 0.875, '7/8 acres': 0.875, '7/8-acres': 0.875,
                '1/5': 0.2, '1/5acre': 0.2, '1/5 acre': 0.2, '1/5-acre': 0.2, '1/5acres': 0.2, '1/5 acres': 0.2, '1/5-acres': 0.2,
                '2/5': 0.4, '2/5acre': 0.4, '2/5 acre': 0.4, '2/5-acre': 0.4, '2/5acres': 0.4, '2/5 acres': 0.4, '2/5-acres': 0.4,
                '3/5': 0.6, '3/5acre': 0.6, '3/5 acre': 0.6, '3/5-acre': 0.6, '3/5acres': 0.6, '3/5 acres': 0.6, '3/5-acres': 0.6,
                '4/5': 0.8, '4/5acre': 0.8, '4/5 acre': 0.8, '4/5-acre': 0.8, '4/5acres': 0.8, '4/5 acres': 0.8, '4/5-acres': 0.8,
                '1/6': 0.1667, '1/6acre': 0.1667, '1/6 acre': 0.1667, '1/6-acre': 0.1667, '1/6acres': 0.1667, '1/6 acres': 0.1667, '1/6-acres': 0.1667,
                '5/6': 0.8333, '5/6acre': 0.8333, '5/6 acre': 0.8333, '5/6-acre': 0.8333, '5/6acres': 0.8333, '5/6 acres': 0.8333, '5/6-acres': 0.8333,
                '1/10': 0.1, '1/10acre': 0.1, '1/10 acre': 0.1, '1/10-acre': 0.1, '1/10acres': 0.1, '1/10 acres': 0.1, '1/10-acres': 0.1,
                '9/10': 0.9, '9/10acre': 0.9, '9/10 acre': 0.9, '9/10-acre': 0.9, '9/10acres': 0.9, '9/10 acres': 0.9, '9/10-acres': 0.9,
                '3/8': 0.375, '3/8acre': 0.375, '3/8 acre': 0.375, '3/8-acre': 0.375, '3/8acres': 0.375, '3/8 acres': 0.375, '3/8-acres': 0.375
            }

            for key in fraction:
                if key in matched_text: return fraction[key]

            # Numeric acres (e.g., "27000 acres", "1000 acres", "3.5 acres")
            numeric_match = re.match(r'\b(\d+\.?\d*)\s*(?:acres?|ac|acr|acrs)\b', matched_text, re.IGNORECASE)
            if numeric_match:
                return float(numeric_match.group(1))

            # Hyphenated numeric acres (e.g., "27000-Acre", "1.25-Acre")
            hyphen_match = re.match(r'\b(\d+\.?\d*)\s*-?(?:[Aa]cre|[Aa]cres|ac|acr|acrs)\b', matched_text, re.IGNORECASE)
            if hyphen_match:
                return float(hyphen_match.group(1))

            # Hectares (e.g., "0.05 ha")
            hectare_match = re.match(r'\b(\d+\.?\d*)\s*-?(?:ha|hectares?)\b', matched_text, re.IGNORECASE)
            if hectare_match:
                return float(hectare_match.group(1)) * 2.471

            # Dimensions (e.g., "50x100 ft", "40 by 80")
            dim_match = re.match(r'\b(\d+\.?\d*)\s*(?:[x*×#/-]|by)\s*(\d+\.?\d*)\s*(?:ft|feet|fts|m)?\b', matched_text, re.IGNORECASE)
            if dim_match:
                length, width = map(float, dim_match.groups())
                return (length * width) / 43560.0

            # Specific ft format (e.g., "50 ft * 100 ft")
            ft_match = re.match(r'\b(\d+)\s*ft\s*\*\s*(\d+)\s*ft\b', matched_text, re.IGNORECASE)
            if ft_match:
                length, width = map(float, ft_match.groups())
                return (length * width) / 43560.0

            # Edge case: "slightly more than a quarter acre"
            if re.match(r'\b(?:slightly\s+more\s+than\s+a\s+quarter)\s*(?:acre|acres|ac|acr|acrs)\b', matched_text, re.IGNORECASE):
                return 0.25

            return np.nan 

        try:
            df['acreage'] = df['size'].apply(map_to_acres)
            logger.info("Successfully created 'acreage' column with converted values")
            df.dropna(subset=['acreage'], inplace=True)
            return df
        except Exception as e:
            logger.error(f"Error converting sizes to acreage: {str(e)}")
            raise e
    
    @staticmethod
    def clean_price(df: pd.DataFrame) -> pd.DataFrame:
        """
        Cleans a price DataFrame by removing the 'price_view' column (if it exists) 
        and renaming the 'price' column to 'price_in_KES'. Calculates price_per_acre(KES).
        """
        try:
            if 'price_view' in df.columns:
                df = df.drop(columns='price_view')
                df.rename(columns={'price': 'price_in_KES'}, inplace=True)
                df['price_per_acre(KES)'] = df.apply(
                    lambda row: np.nan if pd.isna(row['acreage']) or row['acreage'] <= 0 
                    else row['price_in_KES'] / row['acreage'] if pd.isna(row['price_period']) or row['price_period'].strip() != 'per Acre' 
                    else row['price_in_KES'],
                    axis=1
                )
                logger.info("Cleaning Success !! price_view_col dropped, price column cleaned")
            return df
        except Exception as e:
            logger.error("Error!! Failed to clean price columns")
            raise e
    
    @staticmethod
    def enhanced_fraction_parsing(df: pd.DataFrame) -> pd.DataFrame:
        """
        Preprocesses the 'size' column to handle fraction formats like '1/8acre'.
        """
        try:
            fraction_pattern = re.compile(
                r'\b(\d+)/(\d+)(?:\s*th)?(?:\s*|-)?(?:acre|acres|ac|acr|acrs)\b',
                re.IGNORECASE
            )
            
            def preprocess_size(size):
                if pd.isna(size):
                    return size
                text = str(size).lower().strip()
                match = fraction_pattern.search(text)
                if match:
                    num, denom = map(int, match.groups())
                    return f"{num}/{denom} acre"
                return size

            df['size'] = df['size'].apply(preprocess_size)
            logger.info("Successfully preprocessed 'size' column for enhanced fraction parsing")
            return df
        except Exception as e:
            logger.error(f"Error preprocessing size column for fractions: {str(e)}")
            raise e

    def process(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Processes the input DataFrame through all steps.
        """
        try:
            df = self.extract_and_fill_size(df)
            df = self.enhanced_fraction_parsing(df)
            df = self.convert_to_acreage(df)
            df = self.clean_price(df)
        
            logger.info("Successfully processed DataFrame through all steps")
            return df
        except Exception as e:
            logger.error(f"Error processing DataFrame: {str(e)}")
            raise e
        
        


class ExtractVariables(Utilities):
    """This is a class that helps extract features from text descriptions, such as nearness to the road, county, etc."""
    
    def __init__(self):
        super().__init__()
    
    def get_county(self, region):
        """
        Extracts the county name from a region string by matching against known Kenyan counties and their locations.
        
        Args:
            region (str): The region name or text description to analyze.
        
        Returns:
            str or np.nan: The matched county name or np.nan if no match is found.
        """
        if not region or pd.isna(region):
            return np.nan
        for county, locations in self.get_kenyan_counties().items():
            if any(loc.lower() in str(region).lower() for loc in locations):
                return county
        return np.nan
    
    def get_county_population_density(self, county_col):
        """
        county_col: value from df['county'] (can be 'Nairobi', 'Nairobi City', 'nairobi county', etc.)
        Returns the numeric density or np.nan if not found.
        """
        try:
            if pd.isna(county_col) or str(county_col).strip() == "":
                return np.nan

            # normalize input
            county_input = str(county_col).lower()
            county_input = re.sub(r'\bcounty\b', '', county_input)        # remove "county"
            county_input = re.sub(r'[^a-z0-9\s]', ' ', county_input)     # remove punctuation
            county_input = re.sub(r'\s+', ' ', county_input).strip()

            pop_params = self.population_parameters or {}
            # first pass: exact / substring two-way match
            for key, val in pop_params.items():
                key_norm = key.lower()
                key_norm = re.sub(r'\bcounty\b', '', key_norm)
                key_norm = re.sub(r'[^a-z0-9\s]', ' ', key_norm)
                key_norm = re.sub(r'\s+', ' ', key_norm).strip()

                if county_input == key_norm or county_input in key_norm or key_norm in county_input:
                    return val.get("Density (Persons per Sq. Km)", np.nan)

            # second pass: token (word) matching — pick first key that contains any token from input
            tokens = county_input.split()
            for token in tokens:
                for key, val in pop_params.items():
                    if token and token in re.sub(r'[^a-z0-9\s]', ' ', key.lower()):
                        return val.get("Density (Persons per Sq. Km)", np.nan)

            logger.debug(f"No population-density match for county value: '{county_col}' (normalized '{county_input}')")
            return np.nan

        except Exception as e:
            logger.error(f"Error retrieving density for {county_col}: {e}")
            return np.nan
    
    @staticmethod
    def clean_time_on_jiji(time_on_jiji_col):
        try:
            years_pattern = re.compile(r'\d*\s*y')
            months_pattern = re.compile(r'\d*\s*m', re.I)
            
            y_match = re.search(years_pattern, time_on_jiji_col)
            if y_match:
                years = int(str(y_match.group(0).split(" ")[0]))
            else: 
                years = 0
            m_match = re.search(months_pattern, time_on_jiji_col)
            if m_match:
                months = float(str(m_match.group(0).split(" ")[0]))
            else:
                months = 0
            return years + float(months/12)
        except Exception as e:
            logger.error("Error while cleaning the column time on jiji")
            raise e
            


    def _apply(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Applies county extraction to the DataFrame, using 'region_name' and other columns if available.
        
        Args:
            df (pd.DataFrame): Input DataFrame containing region-related columns.
        
        Returns:
            pd.DataFrame: DataFrame with a new 'county' column.
        """
        try:
            # First attempt: Extract county from 'region_name'
            df['county'] = df['region_name'].apply(self.get_county)
    
            # For rows where county is still NaN, try combining other columns
            mask = df['county'].isna()
            if mask.any():
                def combine_columns(row):
                    columns = ['region_name', 'region_parent_name', 'listing_by']
                    text = ' '.join(str(row[col]) for col in columns if col in df.columns and pd.notna(row[col]))
                    return self.get_county(text)
                
                df.loc[mask, 'county'] = df[mask].apply(combine_columns, axis=1)
                
            df['county_population_density(2019)'] = df['county'].apply(self.get_county_population_density)
            logger.info("Successfully extracted county information")
            df["years_on_jiji"] = df['time_on_jiji'].apply(self.clean_time_on_jiji)
            df.drop(columns= ['time_on_jiji'], inplace= True)
            logger.info("Successfully extracted and cleaned time on jiji")
            return df
        except Exception as e:
            logger.error(f"Error extracting county information: {str(e)}")
            raise e
    
    
    def extract(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Processes the input DataFrame by applying feature extraction.
        
        Args:
            df (pd.DataFrame): Input DataFrame.
        
        Returns:
            pd.DataFrame: Processed DataFrame with extracted features.
        """
        try:
            df = self._apply(df)
            logger.info("Successfully processed DataFrame in ExtractVariables")
            return df
        except Exception as e:
            logger.error(f"Error processing DataFrame in ExtractVariables: {str(e)}")
            raise e