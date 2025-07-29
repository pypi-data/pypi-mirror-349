import pydantic
from typing import Any, Dict, List, Optional
from pydantic import ConfigDict, computed_field, Field
import logging

logger = logging.getLogger(__name__)


class Feedback(pydantic.BaseModel):
    """
    Feedback is the feedback that is sent to the tracking service.
    """

    score: Optional[float] = None
    analysis: Optional[str] = None
    metric_score: Optional[float] = None
    metric_analysis: Optional[str] = None
    metric_confidence: Optional[float] = None
    thumb: Optional[str] = None
    comment: Optional[str] = None


class TrackingEvent(pydantic.BaseModel):
    """
    TrackingEvent is the event that is sent to the tracking service.

    NOTE: the tracking event is one to one mapping to the TrackingEvent API request body.
    """

    run_type: str
    event_name: str
    run_id: str
    task_id: str
    prompt_version: str
    session_id: Optional[str] = None
    parent_run_id: Optional[str] = None
    model_name: Optional[str] = None
    input_messages: Optional[List[Dict[str, Any]]] = None
    output_message: Optional[Dict[str, Any]] = None
    prompt_template: Optional[List[Dict[str, Any]]] = None
    variables: Optional[Dict[str, str]] = None
    error: Optional[Dict[str, Any]] = None
    token_usage: Optional[Dict[str, Any]] = None
    tags: Optional[List[str]] = None
    params: Optional[Dict[str, Any]] = None
    properties: Optional[Dict[str, Any]] = None
    feedback: Optional[Feedback] = None
    timestamp: Optional[str] = None


class PromptVersion(pydantic.BaseModel):
    task_id: str
    version: str
    messages: Optional[List[Dict[str, Any]]] = None
    variable_names: Optional[List[str]] = None
    model_name: str
    temperature: float
    top_p: float
    criteria: str = Field(default='', description='The criteria for the prompt', alias='eval_dimension')

    model_config = ConfigDict(populate_by_name=True)

    # TODO: support multi-turn template
    @computed_field
    def prompt_template(self) -> Optional[str]:  # only for single turn template # type: ignore
        print(f'self.messages = {self.messages}')
        if self.messages and len(self.messages) > 0:
            content = self.messages[0].get('content', self.messages[0].get('Content', None))
            if content and isinstance(content, str):
                return content  # type: ignore
            elif content and isinstance(content, list):
                for message in content:
                    if message.get('type') == 'text':
                        return message.get('text')  # type: ignore
                    elif message.get('Type') == 'text':
                        return message.get('Text')  # type: ignore
        if self.messages:
            logger.error(f'No prompt template found in messages: {self.messages}')
        return None
