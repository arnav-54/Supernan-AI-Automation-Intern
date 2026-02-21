import argparse
import os
from core.media_utils import extract_video_segment, extract_audio
from core.transcribe import transcribe_audio
from core.translate import translate_to_hindi
