import hashlib
import os
import bencodepy


def decode(value):
    return bencodepy.decode(value)

def bytes_to_str(data):
    if isinstance(data, bytes):
        return data.decode()
    raise TypeError(f"Type not serializable: {type(data)}")

def create_torrent(file_path, announce_url, output_file):
    piece_length = 2**20  

    with open(file_path, 'rb') as file:
        file_size = os.path.getsize(file_path)

        num_pieces = file_size // piece_length
        if file_size % piece_length:
            num_pieces += 1

        pieces = []
        hasher = hashlib.sha1()
        while True:
            piece_data = file.read(piece_length)
            if not piece_data:
                break
            hasher.update(piece_data)
            pieces.append(hasher.digest())

        metadata = {
            b'announce': announce_url.encode(),  
            b'info': {
                b'name': os.path.basename(file_path).encode(),  
                b'length': file_size,
                b'piece length': piece_length,
                b'pieces': b''.join(pieces),
            }
        }

        encoded_metadata = bencodepy.encode(metadata)

        with open(output_file, 'wb') as torrent_file:
            torrent_file.write(encoded_metadata)

        decoded = decode(encoded_metadata)
        decoded_str_keys = {bytes_to_str(k): v for k, v in decoded.items()}

        tracker_url = decoded_str_keys['announce'].decode()
        print(f"Tracker URL: {tracker_url}")

        info = decoded_str_keys['info']
        print(f"Length: {info[b'length']}")

        res = str(hashlib.sha1(encoded_metadata).hexdigest())
        print(
            "Info Hash: "
            + str(res)
        )

        info_hash = hashlib.sha1(encoded_metadata).hexdigest()
        return info_hash

def get_info_hash(file_path, announce_url):
    piece_length = 2**20
    with open(file_path, 'rb') as file:
        file_size = os.path.getsize(file_path)

        num_pieces = file_size // piece_length
        if file_size % piece_length:
            num_pieces += 1

        pieces = []
        hasher = hashlib.sha1()
        while True:
            piece_data = file.read(piece_length)
            if not piece_data:
                break
            hasher.update(piece_data)
            pieces.append(hasher.digest())

        metadata = {
            b'announce': announce_url.encode(),  
            b'info': {
                b'name': os.path.basename(file_path).encode(),  
                b'length': file_size,
                b'piece length': piece_length,
                b'pieces': b''.join(pieces),
            }
        }

        encoded_metadata = bencodepy.encode(metadata)
        return str(hashlib.sha1(encoded_metadata).hexdigest())
