#!/usr/bin/env python3
"""
Website Content Scraper and Trainer for Kiatech Software Chatbot
Automatically scrapes website content and trains the chatbot
"""
import requests
from bs4 import BeautifulSoup
import json
import time
import re
from urllib.parse import urljoin, urlparse
from typing import List, Dict, Set
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from app.knowledge_base import KnowledgeBase

class WebsiteScraper:
    """Scraper for extracting content from kiatechsoftware.com"""
    
    def __init__(self, base_url: str = "https://www.kiatechsoftware.com"):
        self.base_url = base_url
        self.domain = urlparse(base_url).netloc
        self.visited_urls: Set[str] = set()
        self.scraped_content: List[Dict] = []
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        })
    
    def is_valid_url(self, url: str) -> bool:
        """Check if URL is valid and belongs to our domain"""
        try:
            parsed = urlparse(url)
            return (
                parsed.netloc == self.domain and
                not any(ext in url.lower() for ext in ['.pdf', '.jpg', '.png', '.gif', '.css', '.js', '.xml', '.zip']) and
                '#' not in url
            )
        except:
            return False
    
    def clean_text(self, text: str) -> str:
        """Clean and normalize text content"""
        if not text:
            return ""
        
        # Remove extra whitespace and normalize
        text = re.sub(r'\s+', ' ', text.strip())
        
        # Remove common navigation and footer text
        unwanted_patterns = [
            r'cookie policy',
            r'privacy policy',
            r'terms of service',
            r'follow us on',
            r'subscribe to',
            r'newsletter',
            r'copyright',
            r'all rights reserved'
        ]
        
        for pattern in unwanted_patterns:
            text = re.sub(pattern, '', text, flags=re.IGNORECASE)
        
        return text.strip()
    
    def extract_page_content(self, url: str) -> Dict:
        """Extract meaningful content from a webpage"""
        try:
            print(f"Scraping: {url}")
            response = self.session.get(url, timeout=10)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Remove script and style elements
            for script in soup(["script", "style", "nav", "footer", "header"]):
                script.decompose()
            
            # Extract title
            title = soup.find('title')
            title_text = title.get_text().strip() if title else "No Title"
            
            # Extract main content
            content_selectors = [
                'main', 'article', '.content', '.main-content', 
                '.page-content', '#content', '.container'
            ]
            
            main_content = ""
            for selector in content_selectors:
                content_elem = soup.select_one(selector)
                if content_elem:
                    main_content = content_elem.get_text()
                    break
            
            if not main_content:
                # Fallback to body content
                body = soup.find('body')
                if body:
                    main_content = body.get_text()
            
            # Clean the content
            cleaned_content = self.clean_text(main_content)
            
            # Extract headings for structure
            headings = []
            for tag in soup.find_all(['h1', 'h2', 'h3', 'h4', 'h5', 'h6']):
                heading_text = self.clean_text(tag.get_text())
                if heading_text and len(heading_text) > 3:
                    headings.append({
                        'level': tag.name,
                        'text': heading_text
                    })
            
            # Extract links for further crawling
            links = []
            for link in soup.find_all('a', href=True):
                href = link['href']
                full_url = urljoin(url, href)
                if self.is_valid_url(full_url) and full_url not in self.visited_urls:
                    link_text = self.clean_text(link.get_text())
                    if link_text and len(link_text) > 2:
                        links.append({
                            'url': full_url,
                            'text': link_text
                        })
            
            return {
                'url': url,
                'title': title_text,
                'content': cleaned_content,
                'headings': headings,
                'links': links,
                'word_count': len(cleaned_content.split()),
                'scraped_at': time.strftime('%Y-%m-%d %H:%M:%S')
            }
            
        except Exception as e:
            print(f"Error scraping {url}: {e}")
            return None
    
    def crawl_website(self, max_pages: int = 50, delay: float = 1.0) -> List[Dict]:
        """Crawl the entire website starting from base URL"""
        print(f"Starting website crawl of {self.base_url}")
        print(f"Max pages: {max_pages}, Delay: {delay}s")
        
        # Start with base URL and add specific product pages we know about
        urls_to_visit = [
            self.base_url,
            f"{self.base_url}/Home/AboutUs",
            f"{self.base_url}/Home/ContactUs",
            f"{self.base_url}/Product",  # EIMS product page
            f"{self.base_url}/Home/Products",  # Products page
            f"{self.base_url}/Home/Services",  # Services page
            f"{self.base_url}/Home/Portfolio",  # Portfolio page
        ]
        self.scraped_content = []
        
        while urls_to_visit and len(self.scraped_content) < max_pages:
            current_url = urls_to_visit.pop(0)
            
            if current_url in self.visited_urls:
                continue
            
            self.visited_urls.add(current_url)
            
            # Extract content from current page
            page_data = self.extract_page_content(current_url)
            
            if page_data and page_data['content']:
                self.scraped_content.append(page_data)
                
                # Add new links to visit
                for link in page_data['links']:
                    if link['url'] not in self.visited_urls and link['url'] not in urls_to_visit:
                        urls_to_visit.append(link['url'])
                
                print(f"✓ Scraped: {page_data['title']} ({page_data['word_count']} words)")
            
            # Be respectful - add delay between requests
            time.sleep(delay)
        
        print(f"\nCrawl complete! Scraped {len(self.scraped_content)} pages")
        return self.scraped_content
    
    def save_scraped_data(self, filename: str = "website_content.json"):
        """Save scraped data to JSON file"""
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(self.scraped_content, f, indent=2, ensure_ascii=False)
        print(f"Scraped data saved to {filename}")
    
    def analyze_content(self) -> Dict:
        """Analyze scraped content for insights"""
        if not self.scraped_content:
            return {}
        
        total_words = sum(page['word_count'] for page in self.scraped_content)
        pages_by_type = {}
        
        # Categorize pages by URL patterns
        for page in self.scraped_content:
            url = page['url']
            if '/product' in url.lower() or '/service' in url.lower():
                page_type = 'products_services'
            elif '/about' in url.lower():
                page_type = 'about'
            elif '/contact' in url.lower():
                page_type = 'contact'
            elif '/blog' in url.lower() or '/news' in url.lower():
                page_type = 'blog_news'
            else:
                page_type = 'general'
            
            if page_type not in pages_by_type:
                pages_by_type[page_type] = []
            pages_by_type[page_type].append(page)
        
        return {
            'total_pages': len(self.scraped_content),
            'total_words': total_words,
            'pages_by_type': pages_by_type,
            'average_words_per_page': total_words / len(self.scraped_content) if self.scraped_content else 0
        }

class WebsiteTrainer:
    """Trainer for converting website content into chatbot knowledge"""
    
    def __init__(self, knowledge_base: KnowledgeBase = None):
        self.knowledge_base = knowledge_base or KnowledgeBase()
    
    def process_scraped_content(self, scraped_data: List[Dict]) -> Dict:
        """Process scraped content and add to knowledge base"""
        print("Processing scraped content for chatbot training...")
        
        facts = []
        example_conversations = []
        product_info = []
        
        for page in scraped_data:
            url = page['url']
            title = page['title']
            content = page['content']
            
            # Extract facts from content
            if content and len(content) > 50:
                facts.append(f"From {title}: {content[:500]}...")
            
            # Create example conversations based on page content
            if '/product' in url.lower() or '/service' in url.lower():
                # Extract product/service information
                product_info.append({
                    'title': title,
                    'url': url,
                    'content': content[:1000]  # First 1000 chars
                })
                
                # Create example Q&A pairs
                example_conversations.extend(self._create_product_examples(title, content))
            
            elif '/about' in url.lower():
                # Create about company examples
                example_conversations.extend(self._create_about_examples(content))
        
        # Add processed content to knowledge base
        for fact in facts:
            self.knowledge_base.add_fact(fact)
        
        for conversation in example_conversations:
            self.knowledge_base.add_example_conversation(
                conversation['user'],
                conversation['assistant']
            )
        
        # Knowledge base auto-saves when adding content
        
        return {
            'facts_added': len(facts),
            'conversations_added': len(example_conversations),
            'products_processed': len(product_info),
            'product_info': product_info
        }
    
    def _create_product_examples(self, title: str, content: str) -> List[Dict]:
        """Create example conversations for product pages"""
        examples = []
        
        # Extract key information
        if 'mobile app' in content.lower():
            examples.append({
                'user': f"Tell me about {title}",
                'assistant': f"Based on our website, {title} involves mobile app development services. We specialize in creating custom mobile applications for both Android and iOS platforms."
            })
        
        if 'web development' in content.lower() or 'web app' in content.lower():
            examples.append({
                'user': "Do you do web development?",
                'assistant': f"Yes! We offer comprehensive web development services. {title} is one of our key offerings, providing custom web applications and solutions."
            })
        
        return examples
    
    def _create_about_examples(self, content: str) -> List[Dict]:
        """Create example conversations for about page"""
        examples = []
        
        if 'kiatech' in content.lower():
            examples.append({
                'user': "Tell me about Kiatech Software",
                'assistant': f"Kiatech Software is a leading software development company. {content[:200]}..."
            })
        
        return examples

def main():
    """Main function to scrape website and train chatbot"""
    print("🚀 Kiatech Software Website Scraper & Trainer")
    print("=" * 60)
    
    # Initialize scraper
    scraper = WebsiteScraper("https://www.kiatechsoftware.com")
    
    # Crawl website
    scraped_data = scraper.crawl_website(max_pages=30, delay=1.0)
    
    if not scraped_data:
        print("❌ No content scraped. Please check the website URL.")
        return
    
    # Save raw data
    scraper.save_scraped_data("kiatech_website_content.json")
    
    # Analyze content
    analysis = scraper.analyze_content()
    print(f"\n📊 Content Analysis:")
    print(f"Total pages: {analysis['total_pages']}")
    print(f"Total words: {analysis['total_words']}")
    print(f"Average words per page: {analysis['average_words_per_page']:.0f}")
    
    # Train chatbot
    trainer = WebsiteTrainer()
    training_results = trainer.process_scraped_content(scraped_data)
    
    print(f"\n🎓 Training Results:")
    print(f"Facts added: {training_results['facts_added']}")
    print(f"Example conversations added: {training_results['conversations_added']}")
    print(f"Products processed: {training_results['products_processed']}")
    
    print(f"\n✅ Website training complete!")
    print(f"Your chatbot now knows about your website content!")

if __name__ == "__main__":
    main()
