import database

def fill_names():
    names = {
        'ESP': {
            1: "Unai Simón", 3: "Robin Le Normand", 10: "Lamine Yamal", 
            16: "Rodri", 7: "Álvaro Morata", 11: "Nico Williams", 20: "Dani Carvajal"
        },
        'ARG': {
            1: "Dibu Martínez", 10: "Lionel Messi", 11: "Ángel Di María", 
            22: "Lautaro Martínez", 9: "Julián Álvarez", 7: "Rodrigo de Paul"
        },
        'BRA': {
            1: "Alisson", 10: "Rodrygo", 7: "Vinícius Jr.", 17: "Endrick"
        },
        'FRA': {
            1: "Maignan", 10: "Kylian Mbappé", 7: "Antoine Griezmann", 11: "Ousmane Dembélé"
        },
        'POR': {
            1: "Diogo Costa", 7: "Cristiano Ronaldo", 10: "Bernardo Silva", 8: "Bruno Fernandes"
        }
    }
    
    for equipo, players in names.items():
        for num, nombre in players.items():
            database.update_cromo_name('MarcosDB12', f"{equipo} {num}", nombre)
            print(f"Updated {equipo} {num}: {nombre}")

if __name__ == '__main__':
    fill_names()
