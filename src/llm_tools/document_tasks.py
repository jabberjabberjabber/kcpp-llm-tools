from typing import List, Dict, Optional, Union
from pathlib import Path
from datetime import datetime
import asyncio
import json

from .chunking.processor import ChunkingProcessor
from .core.core import LLMToolsCore

class DocumentTasks:
    """ Handles high-level document processing tasks """
    
    def __init__(self, core: LLMToolsCore):
        """ Initialize document processor
        """
        self.core = core
        self.max_context = self.core.api_client.get_max_context_length()
        self._setup_tasks()
        
    def _setup_tasks(self):
        """ Configure task parameters """

        base_size = self.max_context
        
        self.task_configs = {
            'translate': {
                'chunk_size': int(base_size * 0.4),  # Translation may expand significantly
                'instruction': (
                    f"Translate the text into {self.core.config.translation_language}. "
                    "Maintain linguistic flourish and authorial style as much as possible. "
                    "Write the full contents without condensing the writing or modernizing the language."
                )
            },
            'summary': {
                'chunk_size': int(base_size * 0.8),  # Summary compresses, can handle more input
                'instruction': (
                    "Extract the key points, themes and actions from the text succinctly "
                    "without developing any conclusions or commentary."
                )
            },
            'correct': {
                'chunk_size': int(base_size * 0.4),  # Corrections roughly 1:1
                'instruction': (
                    "Correct any grammar, spelling, style, or format errors in the text. "
                    "Do not alter the text or otherwise change the meaning or style."
                )
            },
            'distill': {
                'chunk_size': int(base_size * 0.8),  # Like summary, output is compressed
                'instruction': (
                    "Rewrite the text to be as concise as possible without losing meaning."
                )
            }
        }
    
    async def _async_streaming(self, prompt):
        """
            Asynchronous streaming generation
        """
        generated_text = ""
        max_length = self.max_context // 2
        try:
            async for chunk in self.core.api_client.stream_generate(prompt=prompt, max_length=max_length, **self.core.get_generation_params()):
                print(chunk, end='', flush=True)
                generated_text += chunk
            return generated_text
            assert len(generated_text.strip()) > 0, "No text was generated"
        except Exception as e:
            print(f"Async streaming failed: {e}")
            raise

    def process_file(self, task: str, file_path: Union[str, Path]) -> tuple[List[str], Dict]:
        """ Process document from file
        
            Args:
                task: Processing task
                file_path: Path to document file
                
            Returns:
                Tuple of (processed chunks, metadata)
        """
        chunker = ChunkingProcessor(
            self.core.api_client,
            max_chunk_length=self.task_configs[task]['chunk_size']
        )
        chunks, metadata = chunker.chunk_file(file_path)
        
        results = []
        for chunk, _ in chunks:
            wrapped = self.core.template_wrapper.wrap_prompt(
                instruction=self.task_configs[task]['instruction'],
                content=chunk,
                system_instruction="You are a helpful assistant."
            )
            response = asyncio.run(self._async_streaming(wrapped[0]))
            results.append(response)
        print("\n")
        metadata['Processing-Time'] = datetime.now().isoformat()
        metadata['Task'] = task
        
        return results, metadata
        
        