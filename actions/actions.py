import sqlite3
from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet
import logging

def connect_db():
    try:
        connection = sqlite3.connect('C:\\Users\\bacha\\rasarasa\\database.db')
        return connection
    except sqlite3.Error as e:
        logging.error(f"Database connection failed: {e}")
        return None

class ActionListHousesForSale(Action):
    def name(self) -> Text:
        return "action_list_houses_for_sale"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        conn = connect_db()
        if not conn:
            dispatcher.utter_message(text="Failed to connect to the database.")
            return []

        try:
            cursor = conn.cursor()
            cursor.execute("SELECT title, area, price, url FROM real_estate")
            houses = cursor.fetchall()
            
            if houses:
                message = "Voici quelques maisons à vendre :\n"
                for i, house in enumerate(houses, start=1):
                    message += f"{i}- {house[0]} à {house[1]} m² pour ${house[2]}. Plus d'infos: {house[3]}\n"
            else:
                message = "Désolé, il n'y a pas de maisons disponibles à vendre pour le moment."
            
            dispatcher.utter_message(text=message)
        except sqlite3.Error as e:
            logging.error(f"Failed to retrieve houses: {e}")
            dispatcher.utter_message(text="An error occurred while retrieving the houses.")
        finally:
            conn.close()
        
        return []

import logging

class ActionFilterHousesByCity(Action):
    def name(self) -> Text:
        return "action_filter_houses_by_city"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        city = tracker.get_slot('city')
        logging.info(f"City slot value: {city}")

        if not city:
            dispatcher.utter_message(text="Veuillez spécifier la ville qui vous intéresse.")
            return []

        conn = connect_db()
        if not conn:
            dispatcher.utter_message(text="Échec de la connexion à la base de données.")
            return []

        try:
            cursor = conn.cursor()
            query = """
                SELECT title, area, price, url, department, real_estate_type
                FROM real_estate 
                WHERE LOWER(department) = ?
            """
            cursor.execute(query, (city.lower(),))
            houses = cursor.fetchall()

            if houses:
                message = f"Maisons disponibles à {city.title()} :\n"
                for i, house in enumerate(houses, start=1):
                    title, area, price, url, city, real_estate_type = house
                    message += f"{i}- {title} : {area} m² pour {price}€. Plus d'infos : {url}\n"
            else:
                message = f"Désolé, il n'y a pas de maisons disponibles à {city.title()} pour le moment."

        except sqlite3.Error as e:
            logging.error(f"Échec de la recherche des maisons par ville : {e}")
            message = "Une erreur est survenue lors de la récupération des maisons."
        
        finally:
            conn.close()

        dispatcher.utter_message(text=message)
        return []


class ActionListHousesByBudget(Action):
    def name(self) -> Text:
        return "action_list_houses_by_budget"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        budget = tracker.get_slot("budget")
        if budget is None:
            dispatcher.utter_message(text="I need to know your budget to search for houses.")
            return []

        try:
            budget = float(budget)
        except ValueError:
            dispatcher.utter_message(text="Please provide a valid budget.")
            return []

        conn = connect_db()
        if not conn:
            dispatcher.utter_message(text="Failed to connect to the database.")
            return []

        try:
            cursor = conn.cursor()
            cursor.execute("SELECT title, city, price, url FROM real_estate WHERE price <= ?", (budget,))
            houses = cursor.fetchall()

            if houses:
                message = f"Maisons dans votre budget de ${budget} :\n"
                for i, house in enumerate(houses, start=1):
                    message += f"{i}- {house[0]} à {house[1]} pour ${house[2]}. Plus d'infos : {house[3]}\n"
            else:
                message = f"Désolé, il n'y a pas de maisons disponibles dans votre budget de ${budget}."
            
            dispatcher.utter_message(text=message)
        except sqlite3.Error as e:
            logging.error(f"Failed to filter houses by budget: {e}")
            dispatcher.utter_message(text="An error occurred while retrieving the houses.")
        finally:
            conn.close()

        return []

class ActionListHousesByArea(Action):
    def name(self) -> Text:
        return "action_list_houses_by_area"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        area = tracker.get_slot("area")

        if area is None:
            dispatcher.utter_message(text="I need to know the minimal area to search for houses.")
            return []

        try:
            area = float(area)
        except ValueError:
            dispatcher.utter_message(text="Please provide a valid area.")
            return []

        conn = connect_db()
        if not conn:
            dispatcher.utter_message(text="Failed to connect to the database.")
            return []

        try:
            cursor = conn.cursor()
            cursor.execute("SELECT title, price, url FROM real_estate WHERE area >= ?", (area,))
            houses = cursor.fetchall()

            if houses:
                message = f"Maisons disponibles avec au moins {area} m² :\n"
                for i, house in enumerate(houses, start=1):
                    message += f"{i}- {house[0]} pour ${house[1]}. Plus d'infos : {house[2]}\n"
            else:
                message = f"Désolé, il n'y a pas de maisons disponibles avec au moins {area} m²."
            
            dispatcher.utter_message(text=message)
        except sqlite3.Error as e:
            logging.error(f"Failed to filter houses by area: {e}")
            dispatcher.utter_message(text="An error occurred while retrieving the houses.")
        finally:
            conn.close()

        return []

class ActionFilterByHouseSize(Action):
    def name(self) -> Text:
        return "action_filter_by_house_size"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        num_rooms = tracker.get_slot("num_rooms")

        if not num_rooms:
            dispatcher.utter_message(text="Combien de chambres recherchez-vous ?")
            return []

        try:
            num_rooms = int(num_rooms)
        except (TypeError, ValueError):
            dispatcher.utter_message(text="Veuillez spécifier un nombre valide de chambres.")
            return [SlotSet("num_rooms", None)]

        conn = connect_db()
        if not conn:
            dispatcher.utter_message(text="Échec de la connexion à la base de données.")
            return []

        try:
            cursor = conn.cursor()
            query = """
                SELECT title, price 
                FROM real_estate 
                WHERE room_count >= ? 
                AND LOWER(real_estate_type) = 'appartement'
            """
            cursor.execute(query, (num_rooms,))
            houses = cursor.fetchall()

            if houses:
                message = f"Voici quelques appartements avec {num_rooms} chambres disponibles :\n"
                for i, house in enumerate(houses, start=1):
                    message += f"{i}- {house[0]} pour {house[1]}€\n"
            else:
                message = f"Désolé, il n'y a pas d'appartements avec {num_rooms} chambres disponibles pour le moment."
            
            dispatcher.utter_message(text=message)
        except sqlite3.Error as e:
            logging.error(f"Échec du filtrage des maisons par taille: {e}")
            dispatcher.utter_message(text="Une erreur s'est produite lors de la récupération des appartements.")
        finally:
            conn.close()

        return []

class ActionFilterByHouseType(Action):
    def name(self) -> Text:
        return "action_filter_by_house_type"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        house_type = tracker.get_slot('house_type')

        if not house_type:
            dispatcher.utter_message(text="What type of house are you looking for?")
            return []

        conn = connect_db()
        if not conn:
            dispatcher.utter_message(text="Failed to connect to the database.")
            return []

        try:
            cursor = conn.cursor()
            query = """
                SELECT title, area, price, url 
                FROM real_estate 
                WHERE LOWER(real_estate_type) = ?
            """
            cursor.execute(query, (house_type,))
            houses = cursor.fetchall()

            if houses:
                message = f"Voici quelques {house_type}s disponibles :\n"
                for i, house in enumerate(houses, start=1):
                    message += f"{i}- {house[0]} : {house[1]} m² pour ${house[2]}. Plus d'infos : {house[3]}\n"
            else:
                message = f"Désolé, il n'y a pas de {house_type}s disponibles pour le moment."
            
            dispatcher.utter_message(text=message)
        except sqlite3.Error as e:
            logging.error(f"Failed to filter houses by type: {e}")
            dispatcher.utter_message(text="An error occurred while retrieving the houses.")
        finally:
            conn.close()

        return []

# groupi vedette laasmi traba aale ydina
class ActionSelectHouse(Action):
    def name(self) -> Text:
        return "action_select_house"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        selected_house_id = tracker.get_slot("house_choice")  

        if not selected_house_id:
            dispatcher.utter_message(text="Veuillez spécifier le numéro de la maison que vous souhaitez sélectionner.")
            return []

        try:
            selected_house_id = int(selected_house_id)
        except ValueError:
            dispatcher.utter_message(text="Veuillez fournir un numéro valide.")
            return []

        try:
            conn = connect_db()
            cursor = conn.cursor()

            cursor.execute("SELECT id, title, area, price, url FROM real_estate WHERE id=?", (selected_house_id,))
            selected_house = cursor.fetchone()

            if selected_house:
                house_id, title, area, price, url = selected_house

                dispatcher.utter_message(
                    text=f"Vous avez sélectionné : {title}, {area} m², {price}€. Plus d'infos : {url}"
                )

                return [
                    SlotSet("selected_house_id", house_id),
                    SlotSet("selected_house", title),
                    SlotSet("selected_house_area", area),
                    SlotSet("selected_house_price", price),
                    SlotSet("selected_house_url", url)
                ]
            else:
                dispatcher.utter_message(text="Désolé, je n'ai pas trouvé la maison que vous avez sélectionnée.")
        except Exception as e:
            logging.error(f"Erreur lors de la sélection de la maison : {e}")
            dispatcher.utter_message(text="Une erreur est survenue lors de la récupération des informations de la maison. Veuillez réessayer plus tard.")
        finally:
            if conn:
                conn.close()

        return []
