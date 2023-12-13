import ast
import os
import gzip
import base64


def decompress_and_decode(encoded_data):
    try:
        # Decode the base64-encoded data
        decoded_data = base64.b64decode(encoded_data)

        # Decompress the gzip data
        decompressed_data = gzip.decompress(decoded_data)

        # Convert the decompressed data to a string
        decoded_string = decompressed_data.decode('utf-8')

        # Convert the decoded string to a Python dictionary
        return ast.literal_eval(decoded_string)

    except Exception as e:
        # Handle errors during decoding and decompression
        print(f"Error decoding and decompressing data: {e}")
        return {}


def search(data, keyword, search_type):
    results = []
    keyword_lower = keyword.lower()

    # Check if the search keyword meets the minimum character limit
    if len(keyword) < 3:
        print("Search keyword must be at least 3 characters.")
        return results

    for game, info in data.items():
        game_lower = game.lower()
        developer_lower = info.get('developer', '').lower()

        # Check if the keyword matches the game or developer based on search type
        if (search_type == 'game' and keyword_lower in game_lower) or \
                (search_type == 'developer' and keyword_lower in developer_lower):
            results.append((game, info.get('developer'), info.get('link')))

    return results


def clear_console():
    os.system('cls' if os.name == 'nt' else 'clear')


from _database import _database


def main():
    # Load data from the database module
    game_data = decompress_and_decode(_database)

    # Ask for the search type only once when the program starts
    valid_search_types = ['game', 'developer']
    search_type = input(f'Enter search type ({"/".join(valid_search_types)}) or "q" to quit: ').lower()

    # Check if the entered search type is valid
    while search_type not in valid_search_types and search_type != 'q':
        print(f"Invalid search type. Please enter a valid search type ({'/'.join(valid_search_types)}) or 'q' to quit.")
        search_type = input().lower()

    if search_type == 'q':
        return

    while True:
        search_keyword = input(f'Enter a {search_type} name to search or "q" to quit: ')
        if search_keyword.lower() == 'q':
            break

        results = search(game_data, search_keyword, search_type)
        if results:
            # Clear the console before displaying the results
            clear_console()

            for result in results:
                # Print matching results
                print(f'Game: {result[0]}, Developer: {result[1]}, Link: {result[2]}')
        else:
            # Print message for no matching results
            print('No matching results found.')


if __name__ == "__main__":
    main()
