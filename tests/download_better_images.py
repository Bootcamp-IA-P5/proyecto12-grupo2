"""
Script para descargar imágenes adicionales con logos más visibles
"""

import os
import requests

def download_image(url, save_path):
    """Descargar imagen desde URL"""
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        response = requests.get(url, timeout=30, headers=headers)
        response.raise_for_status()
        
        with open(save_path, 'wb') as f:
            f.write(response.content)
        
        print(f"✅ Descargada: {os.path.basename(save_path)}")
        return True
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def main():
    os.makedirs('tests/test_images/logos_reales', exist_ok=True)
    
    # URLs de imágenes con logos más visibles
    # Estas son URLs de ejemplo - pueden cambiar
    test_images = {
        # Nike
        'nike_logo_1.jpg': 'https://images.pexels.com/photos/1280064/pexels-photo-1280064.jpeg?auto=compress&cs=tinysrgb&w=800',
        'nike_logo_2.jpg': 'https://images.pexels.com/photos/2385477/pexels-photo-2385477.jpeg?auto=compress&cs=tinysrgb&w=800',
        
        # Adidas
        'adidas_logo_1.jpg': 'https://images.pexels.com/photos/1456706/pexels-photo-1456706.jpeg?auto=compress&cs=tinysrgb&w=800',
        'adidas_logo_2.jpg': 'https://images.pexels.com/photos/1407354/pexels-photo-1407354.jpeg?auto=compress&cs=tinysrgb&w=800',
        
        # Apple
        'apple_logo_1.jpg': 'https://images.pexels.com/photos/249421/pexels-photo-249421.jpeg?auto=compress&cs=tinysrgb&w=800',
        'apple_logo_2.jpg': 'https://images.pexels.com/photos/1202723/pexels-photo-1202723.jpeg?auto=compress&cs=tinysrgb&w=800',
        
        # BMW
        'bmw_logo_1.jpg': 'https://images.pexels.com/photos/244206/pexels-photo-244206.jpeg?auto=compress&cs=tinysrgb&w=800',
        'bmw_logo_2.jpg': 'https://images.pexels.com/photos/627678/pexels-photo-627678.jpeg?auto=compress&cs=tinysrgb&w=800',
        
        # Coca-Cola
        'cocacola_logo_1.jpg': 'https://images.pexels.com/photos/2775860/pexels-photo-2775860.jpeg?auto=compress&cs=tinysrgb&w=800',
        'cocacola_logo_2.jpg': 'https://images.pexels.com/photos/1292294/pexels-photo-1292294.jpeg?auto=compress&cs=tinysrgb&w=800',
        
        # Starbucks
        'starbucks_logo_1.jpg': 'https://images.pexels.com/photos/374885/pexels-photo-374885.jpeg?auto=compress&cs=tinysrgb&w=800',
        'starbucks_logo_2.jpg': 'https://images.pexels.com/photos/2118042/pexels-photo-2118042.jpeg?auto=compress&cs=tinysrgb&w=800',
        
        # McDonald's
        'mcdonalds_logo_1.jpg': 'https://images.pexels.com/photos/1552635/pexels-photo-1552635.jpeg?auto=compress&cs=tinysrgb&w=800',
        
        # Ferrari
        'ferrari_logo_1.jpg': 'https://images.pexels.com/photos/248747/pexels-photo-248747.jpeg?auto=compress&cs=tinysrgb&w=800',
    }
    
    print("📥 Descargando imágenes con logos más visibles...")
    print("="*60)
    
    downloaded = 0
    for filename, url in test_images.items():
        save_path = os.path.join('tests/test_images/logos_reales', filename)
        
        if os.path.exists(save_path):
            print(f"⏭️  Ya existe: {filename}")
            continue
        
        if download_image(url, save_path):
            downloaded += 1
    
    print("="*60)
    print(f"\n✅ Descargadas {downloaded} imágenes nuevas")
    print(f"📁 Ubicación: tests/test_images/logos_reales/")
    
    # Instrucciones adicionales
    print("\n" + "="*60)
    print("💡 RECOMENDACIONES PARA MEJORES RESULTADOS:")
    print("="*60)
    print("\n1. 📸 Toma tus propias fotos:")
    print("   - Productos con logos visibles (Nike, Adidas, Apple, etc.)")
    print("   - Asegúrate de que el logo sea claro y esté bien iluminado")
    print("   - Guárdalas en: tests/test_images/")
    
    print("\n2. 🔍 Busca imágenes en Google:")
    print("   Búsquedas recomendadas:")
    print("   - '[marca] logo product'")
    print("   - '[marca] shoe close up'")
    print("   - '[marca] bottle can'")
    print("   - '[marca] store sign'")
    
    print("\n3. 📦 Marcas disponibles en el modelo (27 total):")
    brands = [
        "Adidas", "Apple", "BMW", "Citroen", "Coca Cola", "DHL", "Fedex",
        "Ferrari", "Ford", "Google", "HP", "Heineken", "Intel", "McDonalds",
        "Mini", "Nbc", "Nike", "Pepsi", "Porsche", "Puma", "Red Bull",
        "Sprite", "Starbucks", "Texaco", "Unicef", "Vodafone", "Yahoo"
    ]
    print("   " + ", ".join(brands))
    
    print("\n" + "="*60)

if __name__ == "__main__":
    main()
