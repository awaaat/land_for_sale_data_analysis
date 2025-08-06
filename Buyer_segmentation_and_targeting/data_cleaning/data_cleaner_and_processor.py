import logging
import logging.handlers
import os
import pandas as pd
from datetime import datetime# Logger configuration
import re
import numpy as np

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
    def extract_and_fill_size(df: pd.DataFrame)-> pd.DataFrame:
        """
        Extracts property size information from text fields and populates a new 'size' column in the DataFrame.

        This function searches for size-related patterns (e.g., acres, dimensions, fractions) 
        within the 'title', 'description', and 'property_details' columns of the input DataFrame. 
        It applies regex-based pattern matching to extract relevant size information, 
        drops rows where no match is found, and returns the updated DataFrame.

        Parameters:
            df (pd.DataFrame): Input DataFrame containing property listing information.

        Returns:
            pd.DataFrame: DataFrame with a new 'size' column containing extracted size info, 
        and with rows removed where no size was found.
        """
        pattern = re.compile(
            r"(?:"  # Non-capturing group for all patterns
            r"(?<!\w)(?:quarter|half|one?|two|three*?|four|for(t(h)?)?|five|fif(t(h)?)?|six(t(h)?)?|seven(t(h)?s?)?|eigh(t(h)?)?|nine(t(h)?)?|ten(t(h)?s?)?|eleven|twelve|thirteen|fourteen|fifteen|twenty|thirty|forty|fifty)(?:th|rd|nd|s)?\s*(?:an\s+)?(?:acre|acres|ac|acr|acrs)(?!\w)|"  # Written numbers with optional suffixes (e.g., "eighth acre", "quarter an acre", "two acres")
            r"(?<!\w)(?:[Qq]uarter|[Hh]alf|[Oo]ne|[Tt]wo|[Tt]hree|[Ff]our|[Ff]ive|[Ss]ix|[Ss]even|[Ee]ight|[Nn]ine|[Tt]en|[Ee]leven|[Tt]welve|[Tt]hirteen|[Ff]ourteen|[Ff]ifteen|[Tt]wenty|[Tt]hirty|[Ff]orty|[Ff]ifty)(?:th|rd|nd|s)?\s*(?:an\s+)?(?:[Aa]cre|[Aa]cres|ac|acr|acrs)(?!\w)|"  # Written numbers with optional suffixes (e.g., "Eighth Acre", "Quarter an Acre", "Two Acres")
            r"\b\d+\.?\d*\s*(?:acres?|ac|acr|acrs|ha|hectares?)\b|"  # Numeric acres/hectares (e.g., "32 acres", "4.4acres", "0.75 ac", "5 hectare")
            r"\b\d+\.?\d*-(?:[Aa]cre|[Aa]cres|ac|acr|acrs|ha|[Hh]ectares?)\b|"  # Hyphenated numeric acres (e.g., "40-Acre", "1.25-acre", "5-ac")
            r"\b\d+\.?\d*\s*(?:[x*×#/-]|by)\s*\d+\.?\d*\s*(?:ft|feet|fts|m)?\b|"  # Dimensions (e.g., "50 x 100", "40*80feet", "100#100", "50 by 100fts")
            r"\b\d+/\d+\s*th\s*(?:acre|acres|ac|acr|acrs)\b|"  # Fractions with 'th' (e.g., "1/8th acre", "3/4th ac")
            r"\b\d+/\d+\s*(?:acre|acres|ac|acr|acrs)\b|"  # Fractions without 'th' (e.g., "1/4 acre", "1/2 ac")
            r"\b\d+\s*/\s*(?:acre|acres|ac|acr|acrs)\b|"  # Price per acre (e.g., "650 / acre", "1000 / ac")
            r"\b(?:slightly\s+more\s+than\s+a\s+quarter)\s*(?:acre|acres|ac|acr|acrs)\b|"  # Edge case (e.g., "slightly more than a quarter acre")
            r"\b\d+\s*ft\s*\*\s*\d+\s*ft\b|"  # Specific format with ft (e.g., "50 ft * 100 ft")
            r"\bNumber\s+of\s+plots\s*:\s*\d+\b"  # Number of plots (e.g., "Number of plots: 2")
            r")",
            re.IGNORECASE | re.UNICODE
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
            return  df
        
        except Exception as e:
            logger.error("Error while extracting text matches")
            raise e
        
    @staticmethod 
    def convert_to_acreage(df: pd.DataFrame) -> pd.DataFrame:
        """
        Converts the 'size' column in the DataFrame to acres and populates a new 'acreage' column.

        This function processes the 'size' column (containing values like acres, fractions, dimensions, 
        hectares and converts each to acres as a floating-point number. 
        Invalid entries (e.g., price per acre, "Number of plots") are assigned np.nan.

        Parameters:
            df (pd.DataFrame): Input DataFrame with a 'size' column.

        Returns:
            pd.DataFrame: DataFrame with a new 'acreage' column containing converted values in acres.
        """
        pattern = re.compile(
            r"(?:"  # Non-capturing group for all patterns
            r"\b\d+/\d+\s*th?\s*(?:acre|acres|ac|acr|acrs)\b|"  # Fractions (e.g., "1/4 acre", "1/8th ac")
            r"(?<!\w)(?:quarter|half|one?|two|three*?|four|for(t(h)?)?|five|fif(t(h)?)?|six(t(h)?)?|seven(t(h)?s?)?|eigh(t(h)?)?|nine(t(h)?)?|ten(t(h)?s?)?|eleven|twelve|thirteen|fourteen|fifteen|sixteen|seventeen|eighteen|nineteen|twenty|thirty|forty|fifty|sixty|seventy|eighty|ninety|(?:one|two|three|four|five|six|seven|eight|nine)\s*hundred(?:\s*(?:twenty|thirty|forty|fifty|sixty|seventy|eighty|ninety)?(?:\s*(?:one|two|three|four|five|six|seven|eight|nine))?)?)(?:th|rd|nd|s)?\s*(?:an\s+)?(?:acre|acres|ac|acr|acrs)(?!\w)|"  # Written numbers with optional suffixes
            r"(?<!\w)(?:[Qq]uarter|[Hh]alf|[Oo]ne|[Tt]wo|[Tt]hree|[Ff]our|[Ff]or(t(h)?)?|[Ff]ive|[Ff]if(t(h)?)?|[Ss]ix(t(h)?)?|[Ss]even(t(h)?s?)?|[Ee]igh(t(h)?)?|[Nn]ine(t(h)?)?|[Tt]en(t(h)?s?)?|[Ee]leven|[Tt]welve|[Tt]hirteen|[Ff]ourteen|[Ff]ifteen|[Ss]ixteen|[Ss]eventeen|[Ee]ighteen|[Nn]ineteen|[Tt]wenty|[Tt]hirty|[Ff]orty|[Ff]ifty|[Ss]ixty|[Ss]eventy|[Ee]ighty|[Nn]inety|(?:[Oo]ne|[Tt]wo|[Tt]hree|[Ff]our|[Ff]ive|[Ss]ix|[Ss]even|[Ee]ight|[Nn]ine)\s*[Hh]undred(?:\s*(?:[Tt]wenty|[Tt]hirty|[Ff]orty|[Ff]ifty|[Ss]ixty|[Ss]eventy|[Ee]ighty|[Nn]inety)?(?:\s*(?:[Oo]ne|[Tt]wo|[Tt]hree|[Ff]our|[Ff]ive|[Ss]ix|[Ss]even|[Ee]ight|[Nn]ine))?)?)(?:th|rd|nd|s)?\s*(?:an\s+)?(?:[Aa]cre|[Aa]cres|ac|acr|acrs)(?!\w)|"  # Written numbers (capitalized)
            r"\b\d+\.?\d*\s*\-*?(?:hectare|acres?|ac|acr|acrs|ha|hectares?)\b|"  # Numeric acres/hectares
            r"\b\d+\.?\d*-(?:[Aa]cre|[Aa]cres|ac|acr|acrs|ha|[Hh]ectares?)\b|"  # Hyphenated numeric acres
            r"\b\d+\.?\d*\s*(?:[x*×#/-]|by)\s*\d+\.?\d*\s*(?:ft|feet|fts|m)?\b|"  # Dimensions
            r"\b\d+\s*/\s*(?:acre|acres|ac|acr|acrs)\b|"  # Price per acre
            r"\b(?:slightly\s+more\s+than\s+a\s+quarter)\s*(?:acre|acres|ac|acr|acrs)\b|"  # Edge case
            r"\b\d+\s*ft\s*\*\s*\d+\s*ft\b|"  # Specific ft format
            r"\bNumber\s+of\s+plots\s*:\s*\d+\b"  # Number of plots
            r")",
            re.IGNORECASE | re.UNICODE
        )

        def parse_written_number(text):
            """Parse written numbers from 1 to 1000 (e.g., 'one hundred forty seven' -> 147.0)."""
            written_numbers = {
                'quarter': 0.25, 'half': 0.5, 'on': 1, 'one': 1.0, 'two': 2.0, 'three': 3.0, 'four': 4.0,
                'five': 5.0, 'six': 6.0, 'seven': 7.0, 'eight': 8.0, 'eighth': 0.125, 'nine': 9.0,
                'ten': 10.0, 'eleven': 11.0, 'twelve': 12.0, 'thirteen': 13.0, 'fourteen': 14.0,
                'fifteen': 15.0, 'sixteen': 16.0, 'seventeen': 17.0, 'eighteen': 18.0, 'nineteen': 19.0,
                'twenty': 20.0, 'thirty': 30.0, 'forty': 40.0, 'fifty': 50.0, 'sixty': 60.0,
                'seventy': 70.0, 'eighty': 80.0, 'ninety': 90.0
            }
            hundreds = {f'{n} hundred': i * 100.0 for i, n in enumerate(['', 'one', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight', 'nine'], start=0)}

            # Normalize text
            text = text.lower().replace(' an ', ' ').replace(' and ', ' ').strip()
            text = re.sub(r'(?:th|rd|nd|s)?\s*(?:acre|acres|ac|acr|acrs)\b', '', text).strip()

            # Direct mapping for simple cases
            if text in written_numbers:
                return written_numbers[text]
            if text in hundreds:
                return hundreds[text]

            # Handle decimal numbers (e.g., "1.4")
            decimal_match = re.match(r'^\d+\.\d+$', text)
            if decimal_match:
                return float(text)

            # Handle compound numbers (e.g., "one hundred forty seven")
            parts = text.split()
            total = 0.0
            if len(parts) > 1 and parts[1] == 'hundred':
                hundreds_value = hundreds.get(f'{parts[0]} hundred', 0.0)
                total += hundreds_value
                if len(parts) > 2:
                    # Handle tens and units
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

            # Written numbers, fractions, or decimals (e.g., "quarter", "1/2", "1.4")
            written_match = re.match(r'(?<!\w)(\d+/\d+|\d+\.\d+|quarter|half|one*?|two|three*?|four|five|six|seven|eigh(?:t|th)|nine|ten|eleven|twelve|thirteen|fourteen|fifteen|sixteen|seventeen|eighteen|nineteen|twenty|thirty|forty|fifty|sixty|seventy|eighty|ninety|(?:one|two|three|four|five|six|seven|eight|nine)\s+hundred(?:\s*(?:twenty|thirty|forty|fifty|sixty|seventy|eighty|ninety)?(?:\s*(?:one|two|three|four|five|six|seven|eight|nine))?)?)(?:th|rd|nd|s)?\s*(?:an\s+)?(?:acre|acres|ac|acr|acrs)(?!\w)', matched_text, re.IGNORECASE)
            if written_match:
                parsed_value = parse_written_number(written_match.group(1))
                if parsed_value is not None:
                    return parsed_value
            #string fractions
            
            fraction = {'650 / acre':650, '1/2': 0.5, '1/4': 0.25, '1/8': 0.125, '1/3': 0.3333, '2/3': 0.6667, '3/4': 0.75, 
                '5/8': 0.625, '7/8': 0.875, '1/5': 0.2, '2/5': 0.4, '3/5': 0.6, '4/5': 0.8,
                '1/6': 0.1667, '5/6': 0.8333, '1/10': 0.1, '9/10': 0.9, '3/8': 0.375}
            for key in fraction:
                if key in matched_text: return fraction[key]
            # Numeric acres (e.g., "5 Acres", "3.5 ac")
            numeric_match = re.match(r'\b(\d+\.?\d*)\s*(?:acres?|ac|acr|acrs)\b', matched_text, re.IGNORECASE)
            if numeric_match:
                return float(numeric_match.group(1))
            # Hyphenated numeric acres (e.g., "1.25-Acre")
            hyphen_match = re.match(r'\b(\d+\.?\d*)\s*?\-*?(?:[Aa]cre|[Aa]cres|ac|acr|acrs)\b', matched_text, re.IGNORECASE)
            if hyphen_match:
                return float(hyphen_match.group(1))

            # Hectares (e.g., "0.05 ha")
            hectare_match = re.match(r'\b(\d+\.?\d*)\s*\-*(?:ha|hectares?)\b', matched_text, re.IGNORECASE)
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
            return  df
        except Exception as e:
            logger.error(f"Error converting sizes to acreage for '{text}': {str(e)}") # pyright: ignore[reportUndefinedVariable]
            raise e
    
    @staticmethod
    def clean_price(df: pd.DataFrame) -> pd.DataFrame:
        """
        Cleans a price DataFrame by removing the 'price_view' column (if it exists) 
        and renaming the 'price' column to 'price_in_KES'. Calculates price_per_acre(KES)
        based on the stripped price_period value.

        Parameters:
            df (pd.DataFrame): Input DataFrame containing pricing information.

        Returns:
            pd.DataFrame: A cleaned DataFrame with 'price_view' dropped and 
            'price' renamed to 'price_in_KES' with updated price_per_acre.
        """
        try:
            if 'price_view' in df.columns:
                df = df.drop(columns='price_view')
                df.rename(columns={'price': 'price_in_KES'}, inplace=True)
                # Calculate price_per_acre only if not per Acre, with safeguard for zero or NaN acreage
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
    

    def process(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Processes the input DataFrame by sequentially applying size extraction, acreage conversion, and price cleaning.

        Parameters:
            df (pd.DataFrame): Input DataFrame containing property listing information.

        Returns:
            pd.DataFrame: Fully processed DataFrame with 'size', 'acreage', and 'price_in_KES' columns.
        """
        try:
            df = self.extract_and_fill_size(df)
            df = self.convert_to_acreage(df)
            df = self.clean_price(df)
            logger.info("Successfully processed DataFrame through all steps")
            return df
        except Exception as e:
            logger.error(f"Error processing DataFrame: {str(e)}")
            raise e