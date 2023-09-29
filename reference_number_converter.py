class ReferenceNumberConverter:
    SERVICE_TYPES = {
        'a': 'Web Development',
        'b': 'Server Configuration',
        'c': 'Mod Configuration',
        'd': 'JSON',
        'e': 'Map Development',
        'f': '3D Modelling/Texturing',
        'g': 'Bot Development',
        'h': 'Scripting',
        'i': 'Catalog/Pre-made',
        'x': 'Other',
    }

    GAMES = {
        'a': 'DayZ',
        'b': 'Arma',
        'c': 'Discord',
        'x': 'Other',
    }

    @classmethod
    def encode(cls, service_type, discord_id, game, deadline, invoice_no):
        
        service_encode = cls.SERVICE_TYPES.get(service_type)
        game_encode = cls.GAMES.get(game[0])
        
        return f'{service_encode}{discord_id}{game_encode}{deadline}{invoice_no}'

    @classmethod
    def decode(cls, reference_number):
        if len(reference_number) != 21:
            return None  # Invalid reference number length

        service_type = cls.SERVICE_TYPES.get(reference_number[0])
        discord_id = reference_number[1:19]
        game = cls.GAMES.get(reference_number[19])
        deadline = reference_number[20:28]
        invoice_no = reference_number[28:]

        if not service_type or not game:
            return None  # Invalid service type or game code

        return {
            'Service Type': service_type,
            'Discord ID': discord_id,
            'Game': game,
            'Deadline': deadline,
            'Invoice No': invoice_no,
        }