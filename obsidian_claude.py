"""
Obsidian-Claude Connector
Connecte vos notes Obsidian à l'API Claude d'Anthropic
"""

import os
import json
from pathlib import Path
from anthropic import Anthropic
from datetime import datetime

class ObsidianClaude:
    def __init__(self, api_key, vault_path):
        """
        Initialise la connexion entre Obsidian et Claude
        
        Args:
            api_key: Votre clé API Anthropic
            vault_path: Chemin vers votre vault Obsidian
        """
        self.client = Anthropic(api_key=api_key)
        self.vault_path = Path(vault_path)
        self.conversation_history = []
        
    def load_notes(self, search_term=None, limit=10):
        """
        Charge les notes depuis le vault Obsidian
        
        Args:
            search_term: Terme de recherche optionnel
            limit: Nombre maximum de notes à charger
        
        Returns:
            Liste des notes trouvées
        """
        notes = []
        
        # Parcourir tous les fichiers .md dans le vault
        for md_file in self.vault_path.rglob("*.md"):
            try:
                with open(md_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                    
                    # Si recherche, filtrer
                    if search_term is None or search_term.lower() in content.lower():
                        notes.append({
                            'title': md_file.stem,
                            'path': str(md_file.relative_to(self.vault_path)),
                            'content': content,
                            'size': len(content)
                        })
                        
                        if len(notes) >= limit:
                            break
            except Exception as e:
                print(f"Erreur lecture {md_file}: {e}")
                
        return notes
    
    def search_in_notes(self, query):
        """
        Recherche intelligente dans vos notes avec Claude
        
        Args:
            query: Votre question ou recherche
        
        Returns:
            Réponse de Claude basée sur vos notes
        """
        # Charger les notes pertinentes
        notes = self.load_notes(search_term=query, limit=5)
        
        if not notes:
            return "Aucune note trouvée correspondant à votre recherche."
        
        # Préparer le contexte pour Claude
        context = "NOTES OBSIDIAN:\n\n"
        for note in notes:
            context += f"## {note['title']}\n"
            context += f"{note['content'][:1000]}...\n\n"  # Limiter à 1000 caractères par note
        
        # Créer le message pour Claude
        messages = [
            {
                "role": "user",
                "content": f"{context}\n\nQuestion: {query}\n\nRéponds en français en te basant sur les notes ci-dessus."
            }
        ]
        
        # Appeler Claude
        response = self.client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=2000,
            messages=messages
        )
        
        return response.content[0].text
    
    def chat_with_notes(self, message):
        """
        Discute avec Claude en ayant accès à toutes vos notes
        
        Args:
            message: Votre message
        
        Returns:
            Réponse de Claude
        """
        # Charger un échantillon de notes pour le contexte
        notes = self.load_notes(limit=10)
        
        # Créer le contexte
        context = f"Tu as accès à {len(notes)} notes Obsidian. "
        context += "Voici un aperçu:\n\n"
        
        for note in notes[:5]:  # Top 5 notes
            context += f"- {note['title']}: {note['content'][:100]}...\n"
        
        # Ajouter le message à l'historique
        self.conversation_history.append({
            "role": "user",
            "content": message
        })
        
        # Créer les messages avec contexte
        messages_with_context = [
            {
                "role": "user", 
                "content": f"CONTEXTE: {context}\n\nConversation:\n{message}"
            }
        ] + self.conversation_history[1:]  # Historique sans le premier message
        
        # Appeler Claude
        response = self.client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=2000,
            messages=self.conversation_history,
            system=f"Tu es un assistant qui a accès aux notes Obsidian de l'utilisateur. {context}"
        )
        
        assistant_message = response.content[0].text
        
        # Ajouter la réponse à l'historique
        self.conversation_history.append({
            "role": "assistant",
            "content": assistant_message
        })
        
        return assistant_message
    
    def analyze_vault(self):
        """
        Analyse complète de votre vault Obsidian
        
        Returns:
            Analyse détaillée par Claude
        """
        notes = self.load_notes(limit=20)
        
        # Préparer les statistiques
        total_notes = len(list(self.vault_path.rglob("*.md")))
        total_words = sum(len(note['content'].split()) for note in notes)
        
        # Créer un résumé pour Claude
        summary = f"ANALYSE DU VAULT OBSIDIAN:\n\n"
        summary += f"- Total de notes: {total_notes}\n"
        summary += f"- Mots analysés: {total_words}\n\n"
        summary += "Titres des notes:\n"
        
        for note in notes:
            summary += f"- {note['title']} ({note['size']} caractères)\n"
        
        # Demander à Claude d'analyser
        response = self.client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=2000,
            messages=[{
                "role": "user",
                "content": f"{summary}\n\nAnalyse ce vault Obsidian et donne-moi:\n1. Les thèmes principaux\n2. Des suggestions d'organisation\n3. Des idées de connexions entre notes\n\nRéponds en français."
            }]
        )
        
        return response.content[0].text
    
    def generate_note(self, topic, style="détaillé"):
        """
        Génère une nouvelle note avec Claude
        
        Args:
            topic: Sujet de la note
            style: Style d'écriture (détaillé, résumé, bullet points)
        
        Returns:
            Contenu de la note générée
        """
        # Charger des notes similaires pour le contexte
        similar_notes = self.load_notes(search_term=topic, limit=3)
        
        context = ""
        if similar_notes:
            context = "Notes similaires dans ton vault:\n\n"
            for note in similar_notes:
                context += f"## {note['title']}\n{note['content'][:300]}...\n\n"
        
        prompt = f"{context}\n\nCrée une nouvelle note Obsidian sur: {topic}\n"
        prompt += f"Style: {style}\n"
        prompt += "Format: Markdown avec liens [[]], tags #, et sections claires.\n"
        prompt += "Réponds en français."
        
        response = self.client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=3000,
            messages=[{
                "role": "user",
                "content": prompt
            }]
        )
        
        return response.content[0].text
    
    def save_note(self, title, content):
        """
        Sauvegarde une note dans le vault Obsidian
        
        Args:
            title: Titre de la note
            content: Contenu de la note
        """
        # Nettoyer le titre pour le nom de fichier
        safe_title = "".join(c for c in title if c.isalnum() or c in (' ', '-', '_')).strip()
        file_path = self.vault_path / f"{safe_title}.md"
        
        # Ajouter un header avec metadata
        full_content = f"---\ncreated: {datetime.now().strftime('%Y-%m-%d %H:%M')}\ntags: [claude-generated]\n---\n\n"
        full_content += content
        
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(full_content)
        
        return str(file_path)


def main():
    """Fonction principale pour tester"""
    print("🤖 Obsidian-Claude Connector")
    print("=" * 50)
    
    # Charger la configuration
    try:
        with open('config.json', 'r') as f:
            config = json.load(f)
        api_key = config['api_key']
        vault_path = config['vault_path']
    except FileNotFoundError:
        print("❌ Fichier config.json introuvable!")
        print("Créez un fichier config.json avec:")
        print('{"api_key": "votre-clé-api", "vault_path": "/chemin/vers/vault"}')
        return
    
    # Initialiser
    connector = ObsidianClaude(api_key, vault_path)
    
    print(f"✅ Connecté au vault: {vault_path}")
    print("\nCommandes disponibles:")
    print("1. search <terme> - Rechercher dans vos notes")
    print("2. chat <message> - Discuter avec Claude")
    print("3. analyze - Analyser votre vault")
    print("4. generate <sujet> - Générer une nouvelle note")
    print("5. quit - Quitter")
    print("\n" + "=" * 50)
    
    while True:
        command = input("\n💬 Commande: ").strip()
        
        if not command:
            continue
            
        if command.lower() == 'quit':
            print("👋 Au revoir!")
            break
        
        parts = command.split(maxsplit=1)
        cmd = parts[0].lower()
        arg = parts[1] if len(parts) > 1 else ""
        
        try:
            if cmd == 'search':
                if not arg:
                    print("❌ Usage: search <votre recherche>")
                    continue
                print("\n🔍 Recherche en cours...")
                result = connector.search_in_notes(arg)
                print(f"\n📝 Résultat:\n{result}")
                
            elif cmd == 'chat':
                if not arg:
                    print("❌ Usage: chat <votre message>")
                    continue
                print("\n💭 Claude réfléchit...")
                result = connector.chat_with_notes(arg)
                print(f"\n🤖 Claude:\n{result}")
                
            elif cmd == 'analyze':
                print("\n📊 Analyse en cours...")
                result = connector.analyze_vault()
                print(f"\n📈 Analyse:\n{result}")
                
            elif cmd == 'generate':
                if not arg:
                    print("❌ Usage: generate <sujet de la note>")
                    continue
                print("\n✍️ Génération en cours...")
                content = connector.generate_note(arg)
                print(f"\n📄 Note générée:\n{content}")
                
                save = input("\n💾 Sauvegarder dans Obsidian? (o/n): ")
                if save.lower() == 'o':
                    path = connector.save_note(arg, content)
                    print(f"✅ Note sauvegardée: {path}")
                
            else:
                print(f"❌ Commande inconnue: {cmd}")
                
        except Exception as e:
            print(f"❌ Erreur: {e}")


if __name__ == "__main__":
    main()
