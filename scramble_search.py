import sys
import logging
import itertools
import argparse
import time

logging.basicConfig(
    level=logging.INFO  
)

logger = logging.getLogger('scrambled-search')
# allow DEBUG level messages to pass through the logger
#logger.setLevel(logging.DEBUG)

def read_file_to_list(in_file):
    str_list = []
    # read dictionary into a list
    with open(in_file, "r") as f:
        str_list = f.readlines()
    #
    return str_list

def get_scrambled_combinations(dict_word):
    # Create the possible combinations list
    chars_in_search_str = list(dict_word)
    scrambled_combinations = []
    # keep first and last fixed, so we can remove the first and last charaters
    # combinations required for words with length > 3
    # abd - fixed'a' + 'b' + fixed'd' - 3 char words only have 1 combination.
    # ab - both fixed - single combination
    # a - single char - single combination
    if len(chars_in_search_str) > 3:
        first_char = chars_in_search_str[0]
        last_char = chars_in_search_str[-1]
        chars_in_search_str = chars_in_search_str[1:-1]
        n = len(chars_in_search_str)
        logger.debug(f'Generating possibilities for word {chars_in_search_str}')
        
        for permutation in itertools.permutations(chars_in_search_str, n):
            scrambled = ''
            for p in permutation:
                scrambled += str(p)
            #print(scrambled)
            # add the first and last fixed chars
            scrambled = first_char + scrambled + last_char
            scrambled_combinations.append(scrambled)
        #
    else:
        # single combination possible for words of len 3 or less
        scrambled_combinations.append(dict_word)

    return scrambled_combinations

def load_dictionary(dictionary_list):
    scrambled_combinations = []
    key_check = []
    for dict_word in dictionary_list:
        dict_word = dict_word.strip('\n')
        logger.debug(f'Looking for possibilities for word {dict_word}')
        scrambled_list = get_scrambled_combinations(dict_word)
        logger.debug(f'Found {len(scrambled_list)} possibilities for word {dict_word}')
        # save to cached dictionary of scrambled words
        for scrambled_word in scrambled_list:
            dict_key = dict_word + '-' + scrambled_word
            if dict_key in key_check:
                logger.debug(f'Key {dict_key} present already. Skip {dict_key}')
            else:
                key_check.append(dict_key)
                scrambled_combinations.append({
                    'original_word':dict_word,
                    'scrambled_word':scrambled_word
                })
    return scrambled_combinations

def look_for_matches(input_str, scrambled_combinations):
    match_count = 0
    for scrambled in scrambled_combinations:
        if scrambled['scrambled_word'] in input_str.lower():
            match_count += 1
            logger.debug(f'match # {match_count} - {scrambled}')
    return match_count


def run_search(dictionary_list, search_list):
    logger.debug('Running scrambled search')
    # load dictionary once off
    logger.debug('Loading scrambled combinations of dictionary to cache.')
    scrambled_combinations = load_dictionary(dictionary_list)
    line_count = 1
    for input_str in search_list:
        input_str = input_str.strip('\n')
        logger.debug(f'Attempting match for input line {input_str}')
        match_count = look_for_matches(input_str,scrambled_combinations)
        logger.info(f'Case  #{line_count}:{match_count}')
        line_count += 1

def terminate_process():
    sys.exit('Process stopped due to one or more errors.')

def main(argv=None, **kwargs):
    logger.info('Starting process for scrambled search')
    parser = argparse.ArgumentParser(description='Scrambled word search app.')

    # Parse arguments
    parser.add_argument('--dictionary', required=True, help='Path to Dictionary file with list of words to be searched for.')
    parser.add_argument('--input',  required=True, help='Path to input file that provides the text to be searched in.')
    args = parser.parse_args()

    logger.debug(f'Recieved paths for dictionary {args.dictionary}')
    logger.debug(f'Recieved paths for search input {args.input}')

    # Load Dict
    try:
        dictionary_list = read_file_to_list(args.dictionary)
        logger.info(f'Dictionary loaded with {len(dictionary_list)} words.')
        if len(dictionary_list) == 0:
            logger.warning(f'No words found in dictionary')
        else:
            # sum of lengths of all words in the dictionary does not exceed 105.
            dict_size = 0
            for dict_word in dictionary_list:
                dict_size += len(dict_word)
            logger.debug(f'Sum of all lengths of all words in dict =  {dict_size} chars.')
            if dict_size > 105:
                logger.warning(f'Dictionary size exceeds allowed size of 105. Sum of lengths of all words in the dictionary should not exceed 105.')
                terminate_process()
    except:
        logger.error(f'Dictionary file not found at {args.dictionary}')
        terminate_process()

    # Load Search input
    try:
        search_list = read_file_to_list(args.input)
        logger.info(f'Input file loaded with {len(search_list)} lines.')
        if len(search_list) == 0:
            logger.warning(f'No lines found in input file to search')
    except:
        logger.error(f'Input file not found at {args.input}')
        terminate_process()

    # run search process
    start = time.time()
    run_search(dictionary_list, search_list)
    logger.info(f'Completed process for scrambled search, took time {time.time() - start}s')


if __name__ == '__main__':
    logging.getLogger().setLevel(logging.INFO)
    main()