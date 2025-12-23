"""
Script de test pour vérifier que tout fonctionne correctement
"""

import sys
import json
from pathlib import Path

def test_python_version():
    """Teste la version de Python"""
    print("🔍 Test 1: Version Python...")
    version = sys.version_info
    if version.major >= 3 and version.minor >= 8:
        print(f"   ✅ Python {version.major}.{version.minor}.{version.micro} - OK")
        return True
    else:
        print(f"   ❌ Python {version.major}.{version.minor} - Version trop ancienne (besoin 3.8+)")
        return False

def test_anthropic_module():
    """Teste si le module anthropic est installé"""
    print("\n🔍 Test 2: Module Anthropic...")
    try:
        import anthropic
        print(f"   ✅ Module anthropic version {anthropic.__version__} - OK")
        return True
    except ImportError:
        print("   ❌ Module anthropic non installé")
        print("   💡 Solution: pip install anthropic")
        return False

def test_config_file():
    """Teste si le fichier config existe"""
    print("\n🔍 Test 3: Fichier de configuration...")
    config_path = Path("config.json")
    
    if not config_path.exists():
        print("   ❌ Fichier config.json introuvable")
        print("   💡 Solution: Copiez config.example.json en config.json")
        return False
    
    try:
        with open(config_path, 'r') as f:
            config = json.load(f)
        
        if 'api_key' not in config or config['api_key'] == "VOTRE_CLE_API_ANTHROPIC_ICI":
            print("   ❌ Clé API non configurée dans config.json")
            print("   💡 Solution: Ajoutez votre vraie clé API")
            return False
        
        if 'vault_path' not in config:
            print("   ❌ Chemin du vault non configuré")
            print("   💡 Solution: Ajoutez le chemin vers votre vault Obsidian")
            return False
        
        print("   ✅ Fichier config.json - OK")
        return True
        
    except json.JSONDecodeError:
        print("   ❌ Fichier config.json mal formaté")
        print("   💡 Solution: Vérifiez la syntaxe JSON")
        return False

def test_vault_path():
    """Teste si le vault existe"""
    print("\n🔍 Test 4: Vault Obsidian...")
    
    try:
        with open("config.json", 'r') as f:
            config = json.load(f)
        
        vault_path = Path(config['vault_path'])
        
        if not vault_path.exists():
            print(f"   ❌ Vault introuvable: {vault_path}")
            print("   💡 Solution: Vérifiez le chemin dans config.json")
            return False
        
        if not vault_path.is_dir():
            print(f"   ❌ Le chemin n'est pas un dossier: {vault_path}")
            return False
        
        # Compter les fichiers .md
        md_files = list(vault_path.rglob("*.md"))
        
        if len(md_files) == 0:
            print(f"   ⚠️  Vault trouvé mais aucun fichier .md détecté")
            print(f"   💡 Vérifiez que c'est bien le bon dossier")
            return True
        
        print(f"   ✅ Vault trouvé avec {len(md_files)} fichier(s) .md - OK")
        return True
        
    except Exception as e:
        print(f"   ❌ Erreur: {e}")
        return False

def test_api_connection():
    """Teste la connexion à l'API Anthropic"""
    print("\n🔍 Test 5: Connexion API Anthropic...")
    
    try:
        import anthropic
        with open("config.json", 'r') as f:
            config = json.load(f)
        
        client = anthropic.Anthropic(api_key=config['api_key'])
        
        # Test simple
        response = client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=50,
            messages=[{
                "role": "user",
                "content": "Réponds juste 'OK' si tu me reçois"
            }]
        )
        
        print("   ✅ Connexion API réussie - OK")
        print(f"   📝 Réponse de Claude: {response.content[0].text}")
        return True
        
    except anthropic.AuthenticationError:
        print("   ❌ Clé API invalide")
        print("   💡 Vérifiez votre clé sur https://console.anthropic.com")
        return False
    except anthropic.PermissionDeniedError:
        print("   ❌ Accès refusé - vérifiez vos crédits")
        print("   💡 Ajoutez des crédits sur https://console.anthropic.com")
        return False
    except Exception as e:
        print(f"   ❌ Erreur: {e}")
        return False

def main():
    print("=" * 60)
    print("🧪 TEST DE L'INSTALLATION OBSIDIAN-CLAUDE")
    print("=" * 60)
    
    tests = [
        test_python_version(),
        test_anthropic_module(),
        test_config_file(),
        test_vault_path(),
        test_api_connection()
    ]
    
    print("\n" + "=" * 60)
    print("📊 RÉSULTATS")
    print("=" * 60)
    
    passed = sum(tests)
    total = len(tests)
    
    print(f"\nTests réussis: {passed}/{total}")
    
    if passed == total:
        print("\n✅ Tout fonctionne ! Vous pouvez lancer:")
        print("   python obsidian_claude.py")
    else:
        print("\n❌ Certains tests ont échoué. Corrigez les erreurs ci-dessus.")
        print("   Relancez ce test après correction: python test_installation.py")
    
    print("\n" + "=" * 60)

if __name__ == "__main__":
    main()
