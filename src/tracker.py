#!/usr/bin/env python3
"""
CoverageSummarizer - Módulo de Rastreabilidade
INCR-3: Sistema de referências a trechos do texto
"""

from typing import List, Dict, Tuple
import re


class TextTracker:
    """Classe responsável por rastrear e indexar trechos do texto original."""
    
    def __init__(self, text: str):
        """
        Inicializa o tracker com o texto original.
        
        Args:
            text: Texto completo a ser rastreado
        """
        self.original_text = text
        self.text_length = len(text)
        self.words = text.split()
        self.total_words = len(self.words)
        
        # Dividir texto em segmentos para referência
        self.segments = self._create_segments()
    
    def _create_segments(self, segment_size: int = 500) -> List[Dict]:
        """
        Divide o texto em segmentos para referência.
        
        Args:
            segment_size: Tamanho aproximado de cada segmento em palavras
        
        Returns:
            Lista de dicionários com informações dos segmentos
        """
        segments = []
        words = self.words
        
        for i in range(0, len(words), segment_size):
            segment_words = words[i:i + segment_size]
            segment_text = ' '.join(segment_words)
            start_word = i
            end_word = min(i + segment_size, len(words))
            
            # Calcular posição aproximada no texto
            start_char = len(' '.join(words[:i]))
            end_char = len(' '.join(words[:end_word]))
            
            segments.append({
                'id': len(segments) + 1,
                'start_word': start_word,
                'end_word': end_word,
                'start_char': start_char,
                'end_char': end_char,
                'text': segment_text,
                'word_range': f"{start_word}-{end_word}"
            })
        
        return segments
    
    def find_segment_by_text(self, search_text: str, context_words: int = 50) -> List[Dict]:
        """
        Encontra segmentos que contêm o texto pesquisado.
        
        Args:
            search_text: Texto a ser pesquisado
            context_words: Número de palavras de contexto ao redor
        
        Returns:
            Lista de segmentos encontrados com contexto
        """
        search_lower = search_text.lower()
        found_segments = []
        
        for segment in self.segments:
            if search_lower in segment['text'].lower():
                # Adicionar contexto
                start_idx = max(0, segment['start_word'] - context_words)
                end_idx = min(self.total_words, segment['end_word'] + context_words)
                context_text = ' '.join(self.words[start_idx:end_idx])
                
                found_segments.append({
                    'segment_id': segment['id'],
                    'word_range': segment['word_range'],
                    'context': context_text,
                    'exact_match': segment['text']
                })
        
        return found_segments
    
    def get_segment_reference(self, segment_id: int) -> str:
        """
        Retorna referência formatada para um segmento.
        
        Args:
            segment_id: ID do segmento
        
        Returns:
            String com referência formatada
        """
        if 1 <= segment_id <= len(self.segments):
            segment = self.segments[segment_id - 1]
            # Calcular porcentagem aproximada no texto
            position_pct = (segment['start_word'] / self.total_words) * 100
            return f"[Trecho {segment_id}: palavras {segment['word_range']}, ~{position_pct:.1f}% do texto]"
        return "[Referência inválida]"
    
    def extract_key_phrases(self, text: str, max_phrases: int = 10) -> List[str]:
        """
        Extrai frases-chave do texto para melhor rastreabilidade.
        
        Args:
            text: Texto do qual extrair frases
            max_phrases: Número máximo de frases a extrair
        
        Returns:
            Lista de frases-chave
        """
        # Dividir em sentenças
        sentences = re.split(r'[.!?]+', text)
        sentences = [s.strip() for s in sentences if len(s.strip()) > 20]
        
        # Ordenar por comprimento (frases mais longas tendem a ser mais importantes)
        sentences.sort(key=len, reverse=True)
        
        return sentences[:max_phrases]
    
    def create_reference_map(self, summary_text: str) -> Dict[str, List[str]]:
        """
        Cria mapa de referências entre resumo e texto original.
        
        Args:
            summary_text: Texto do resumo
        
        Returns:
            Dicionário mapeando partes do resumo para referências
        """
        # Extrair frases-chave do resumo
        summary_sentences = re.split(r'[.!?]+', summary_text)
        summary_sentences = [s.strip() for s in summary_sentences if len(s.strip()) > 10]
        
        reference_map = {}
        
        for sentence in summary_sentences[:20]:  # Limitar para performance
            # Buscar no texto original
            segments = self.find_segment_by_text(sentence, context_words=30)
            if segments:
                references = [self.get_segment_reference(s['segment_id']) for s in segments[:3]]
                reference_map[sentence[:100]] = references
        
        return reference_map


def format_references(references: List[str]) -> str:
    """
    Formata lista de referências para exibição.
    
    Args:
        references: Lista de referências
    
    Returns:
        String formatada
    """
    if not references:
        return "  [Sem referências específicas]"
    
    formatted = []
    for i, ref in enumerate(references, 1):
        formatted.append(f"  {i}. {ref}")
    
    return "\n".join(formatted)
