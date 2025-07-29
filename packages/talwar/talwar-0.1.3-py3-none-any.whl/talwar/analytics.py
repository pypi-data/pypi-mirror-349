import os
import platform
import uuid
import time
from typing import Dict, Any, Optional
from posthog import Posthog
import logging

logger = logging.getLogger(__name__)

# Set PostHog API key directly for testing
os.environ['POSTHOG_API_KEY'] = 'phc_w602YAivauZg9lk4sUXzEfLM8E4fenUx0h5lYdchshD'

class Analytics:
    """
    Analytics handler for tracking Talwar usage.
    Uses PostHog for anonymous usage tracking.
    """
    
    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize analytics with PostHog.
        
        Args:
            api_key: PostHog API key. If not provided, will look for POSTHOG_API_KEY env var
        """
        self.api_key = api_key or os.getenv('POSTHOG_API_KEY')
        if not self.api_key:
            logger.warning("No PostHog API key found. Analytics will be disabled.")
            return
            
        # Initialize PostHog client
        self.posthog = Posthog(
            self.api_key,
            host='https://app.posthog.com'
        )
        
        # Generate a unique ID for this installation
        self.distinct_id = str(uuid.uuid4())
        
        # Track system info
        self.system_info = {
            'os': platform.system(),
            'python_version': platform.python_version()
        }
        
        # Scan metrics
        self.scan_start_time = None
        self.vulnerabilities_found = 0
        
        # Identify the user
        try:
            self.posthog.identify(
                distinct_id=self.distinct_id,
                properties=self.system_info
            )
        except Exception as e:
            logger.error(f"Failed to identify user in PostHog: {str(e)}")
    
    def track_event(self, event_name: str, properties: Optional[Dict[str, Any]] = None):
        """
        Track an event in PostHog.
        
        Args:
            event_name: Name of the event to track
            properties: Additional properties to track with the event
        """
        if not self.api_key:
            return
            
        if properties is None:
            properties = {}
            
        # Add system info to all events
        properties.update(self.system_info)
        
        try:
            self.posthog.capture(
                distinct_id=self.distinct_id,
                event=event_name,
                properties=properties
            )
        except Exception as e:
            logger.error(f"Failed to track event {event_name}: {str(e)}")
    
    def track_scan_start(self, target_url: str, expand_scope: bool, enumerate_subdomains: bool):
        """Track when a scan starts"""
        self.scan_start_time = time.time()
        self.track_event('scan_started', {
            'target_domain': self._extract_domain(target_url)
        })
    
    def track_scan_complete(self, target_url: str, vulnerabilities_found: int, status: str = 'success'):
        """Track when a scan completes"""
        scan_duration = time.time() - self.scan_start_time if self.scan_start_time else 0
        
        self.track_event('scan_completed', {
            'target_domain': self._extract_domain(target_url),
            'vulnerabilities_found': vulnerabilities_found,
            'scan_duration_seconds': scan_duration,
            'completion_status': status
        })
    
    def track_scan_terminated(self, target_url: str, vulnerabilities_found: int, reason: str):
        """Track when a scan is terminated"""
        scan_duration = time.time() - self.scan_start_time if self.scan_start_time else 0
        
        self.track_event('scan_terminated', {
            'target_domain': self._extract_domain(target_url),
            'vulnerabilities_found': vulnerabilities_found,
            'scan_duration_seconds': scan_duration,
            'termination_reason': reason
        })
    
    def track_vulnerability_found(self, vulnerability_type: str, severity: str):
        """Track when a vulnerability is found"""
        self.vulnerabilities_found += 1
        self.track_event('vulnerability_found', {
            'type': vulnerability_type,
            'severity': severity
        })
    
    def track_error(self, error_type: str, error_message: str, context: str):
        """Track when an error occurs"""
        self.track_event('error_occurred', {
            'error_type': error_type,
            'error_message': error_message,
            'context': context
        })
    
    def _extract_domain(self, url: str) -> str:
        """Extract domain from URL for analytics"""
        try:
            from urllib.parse import urlparse
            parsed = urlparse(url)
            return parsed.netloc
        except:
            return url 