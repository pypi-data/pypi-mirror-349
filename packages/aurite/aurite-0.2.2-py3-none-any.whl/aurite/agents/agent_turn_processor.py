# Copyright (c) 2024-2025 Aurite Inc. All rights reserved.
# SPDX-License-Identifier: MIT
"""
Helper class for processing a single turn in an Agent's conversation loop.
"""

import logging
from typing import (
    List,
    Optional,
    Tuple,
    Dict,
    Any,
    TYPE_CHECKING,
    AsyncGenerator,
)  # Added AsyncGenerator

import json
from jsonschema import validate, ValidationError as JsonSchemaValidationError

# Import necessary types
from anthropic.types import MessageParam, ToolResultBlockParam
from typing import cast  # Added for casting
from .agent_models import AgentOutputMessage
from ..host.host import MCPHost
from ..config.config_models import (
    AgentConfig,
    LLMConfig,
)  # Updated import path, added LLMConfig
# Import specific exceptions if needed for error handling

if TYPE_CHECKING:
    from ..llm.base_client import BaseLLM

logger = logging.getLogger(__name__)


class AgentTurnProcessor:
    """
    Handles the logic for a single turn of interaction within the Agent's
    execution loop, including LLM calls, response parsing, schema validation,
    and tool execution coordination.
    """

    def __init__(
        self,
        config: AgentConfig,
        llm_client: "BaseLLM",
        host_instance: MCPHost,
        current_messages: List[MessageParam],
        tools_data: Optional[List[Dict[str, Any]]],
        effective_system_prompt: Optional[str],
        llm_config_for_override: Optional[LLMConfig] = None,  # New parameter
    ):
        """
        Initializes the turn processor.

        Args:
            config: The AgentConfig for the current agent.
            llm_client: The initialized LLM client instance.
            host_instance: The MCPHost instance.
            current_messages: The current list of messages to be sent to the LLM.
            tools_data: Formatted tool definitions for the LLM.
            effective_system_prompt: The system prompt to use for this turn.
            llm_config_for_override: Optional LLMConfig to pass to the LLM client.
        """
        self.config = config
        self.llm = llm_client
        self.host = host_instance
        self.messages = current_messages
        self.tools = tools_data
        self.system_prompt = effective_system_prompt
        self.llm_config_for_override = llm_config_for_override  # Store new parameter
        self._last_llm_response: Optional[AgentOutputMessage] = (
            None  # Store the raw response
        )
        self._tool_uses_this_turn: List[Dict[str, Any]] = []  # Store tool uses
        logger.debug("AgentTurnProcessor initialized.")

    def get_last_llm_response(self) -> Optional[AgentOutputMessage]:
        """Returns the last raw response received from the LLM for this turn."""
        return self._last_llm_response

    def get_tool_uses_this_turn(self) -> List[Dict[str, Any]]:
        """Returns the details of tools used in this turn."""
        return self._tool_uses_this_turn

    async def process_turn(
        self,
    ) -> Tuple[Optional[AgentOutputMessage], Optional[List[MessageParam]], bool]:
        """
        Processes a single conversation turn.

        1. Makes the LLM call.
        2. Parses the response (AgentOutputMessage).
        3. Handles stop reason (tool use or final response).
        4. Performs schema validation if needed.
        5. Executes tools if requested.
        6. Prepares tool results for the next turn if applicable.

        Returns:
            A tuple containing:
            - The final assistant response (AgentOutputMessage) if the turn ended without tool use, else None.
            - A list of tool result messages (List[MessageParam]) to be added for the next turn, or None.
            - A boolean indicating if this turn resulted in the final response (True) or if the loop should continue (False).
        """
        logger.debug("Processing conversation turn...")
        # --- Placeholder for logic to be moved from Agent.execute_agent ---

        # 1. Make LLM call
        try:
            llm_response: AgentOutputMessage = await self.llm.create_message(
                messages=self.messages,  # type: ignore[arg-type]
                tools=self.tools,
                system_prompt_override=self.system_prompt,
                schema=self.config.config_validation_schema,  # Use renamed field
                llm_config_override=self.llm_config_for_override,  # Pass stored override
            )
        except Exception as e:
            # Handle or re-raise LLM call errors appropriately
            logger.error(f"LLM call failed within turn processor: {e}", exc_info=True)
            # Decide error handling strategy - maybe return an error state?
            # For now, re-raise to be caught by Agent.execute_agent
            raise

        self._last_llm_response = llm_response  # Store the response

        # 2. Process LLM Response
        final_assistant_response: Optional[AgentOutputMessage] = None
        tool_results_for_next_turn: Optional[List[MessageParam]] = None
        is_final_turn = False  # Default to False, set True only on valid final response

        if llm_response.stop_reason == "tool_use":
            # Process tool calls if requested
            tool_results_for_next_turn = await self._process_tool_calls(llm_response)
            # _process_tool_calls also populates self._tool_uses_this_turn
            # is_final_turn remains False
            final_assistant_response = None  # No final response this turn
            logger.debug("Processed tool use request.")

        else:
            # Stop reason is likely 'end_turn' or similar - handle as potential final response
            logger.debug(
                f"Processing potential final response (stop_reason: {llm_response.stop_reason})."
            )
            # Handle final response, including schema validation
            validated_response = self._handle_final_response(llm_response)

            if validated_response is not None:
                # Schema validation passed (or no schema) - this IS the final turn
                final_assistant_response = validated_response
                is_final_turn = True
                logger.debug("Valid final response received.")
            else:
                # Schema validation failed - not the final turn, signal retry needed
                final_assistant_response = None  # No valid final response
                is_final_turn = False
                logger.warning("Schema validation failed. Signaling retry.")
                # ConversationManager loop will handle sending correction message

        logger.debug(f"Turn processed. Is final turn: {is_final_turn}")
        return final_assistant_response, tool_results_for_next_turn, is_final_turn

    async def stream_turn_response(
        self,
    ) -> AsyncGenerator[Dict[str, Any], None]:
        """
        Processes a single conversation turn by streaming events from the LLM,
        handling tool calls inline, and yielding standardized event dictionaries.

        Yields:
            Dict[str, Any]: Standardized event dictionaries for SSE.
                            Includes text_delta, tool_use_start, tool_use_input_delta,
                            tool_use_end, tool_result, tool_execution_error, stream_end.
        """
        logger.debug("Streaming conversation turn...")
        self._tool_uses_this_turn = []  # Reset for this turn

        # active_tool_calls stores information about tools the LLM has started to use in the current turn.
        # The key is the LLM's original content_block_index for the tool_use block.
        active_tool_calls: Dict[int, Dict[str, Any]] = {}

        # SSE Event Indexing Strategy:
        # The 'index' field in the yielded event_data for events like text_block_start, text_delta,
        # tool_use_start, tool_use_input_delta, and content_block_stop will directly correspond to
        # the LLM provider's original content_block.index.
        # For tool_result and tool_execution_error events, the 'index' will also be the
        # original content_block.index of the tool_use block that triggered the tool execution.
        # The frontend primarily uses tool_use_id to associate results with their calls for placement.
        # This approach simplifies backend logic by removing custom frontend-specific index allocation.

        try:
            async for llm_event in self.llm.stream_message(
                messages=self.messages,  # type: ignore[arg-type]
                tools=self.tools,
                system_prompt_override=self.system_prompt,
                schema=self.config.config_validation_schema,  # Though schema less used in streaming
                llm_config_override=self.llm_config_for_override,
            ):
                event_type = llm_event.get("event_type")
                event_data = llm_event.get(
                    "data", {}
                ).copy()  # Use a copy for modification
                llm_event_original_index = event_data.get("index")

                if event_type == "tool_use_start":
                    if llm_event_original_index is not None:
                        active_tool_calls[llm_event_original_index] = {
                            "id": event_data.get("tool_id"),
                            "name": event_data.get("tool_name"),
                            "input_str": "",
                        }
                    else:
                        logger.error(
                            f"Tool_use_start event is missing 'index'. Cannot track tool call. Data: {event_data}"
                        )
                    yield {"event_type": event_type, "data": event_data}

                elif event_type == "tool_use_input_delta":
                    if (
                        llm_event_original_index is not None
                        and llm_event_original_index in active_tool_calls
                    ):
                        json_chunk_data = event_data.get("json_chunk")
                        chunk_to_add = (
                            str(json_chunk_data) if json_chunk_data is not None else ""
                        )
                        active_tool_calls[llm_event_original_index]["input_str"] += (
                            chunk_to_add
                        )
                    else:
                        logger.warning(
                            f"ATP: Received tool_use_input_delta for index {llm_event_original_index} but not found in active_tool_calls or index is None."
                        )
                    yield {"event_type": event_type, "data": event_data}

                elif event_type == "content_block_stop":
                    yield {"event_type": event_type, "data": event_data}  # Yield first

                    if (
                        llm_event_original_index is not None
                        and llm_event_original_index in active_tool_calls
                    ):
                        tool_call_info = active_tool_calls.pop(llm_event_original_index)
                        tool_id = tool_call_info.get("id")
                        tool_name = tool_call_info.get("name")
                        tool_input_str = tool_call_info.get("input_str", "")
                        logger.info(
                            f"Executing tool '{tool_name}' (ID: {tool_id}) from stream with input: {tool_input_str}"
                        )
                        try:
                            cleaned_tool_input_str = (
                                tool_input_str.strip() if tool_input_str else ""
                            )
                            sanitized_tool_input_str = "".join(
                                c
                                for c in cleaned_tool_input_str
                                if 31 < ord(c) < 127 or c in ("\n", "\r", "\t")
                            )
                            string_to_parse = (
                                sanitized_tool_input_str
                                if sanitized_tool_input_str
                                else cleaned_tool_input_str
                            )
                            parsed_input = (
                                json.loads(string_to_parse) if string_to_parse else {}
                            )

                            tool_result_content = await self.host.execute_tool(
                                tool_name=tool_name,
                                arguments=parsed_input,
                                agent_config=self.config,
                            )
                            logger.debug(
                                f"Tool '{tool_name}' executed successfully via stream."
                            )
                            serializable_output: Any
                            if isinstance(tool_result_content, str):
                                serializable_output = tool_result_content
                            elif isinstance(tool_result_content, (list, tuple)):
                                serializable_output = []
                                for item in tool_result_content:
                                    if hasattr(item, "model_dump"):
                                        item_dump = item.model_dump(
                                            mode="json", exclude_none=True
                                        )
                                        if item_dump.get("type") == "text":
                                            item_dump = {
                                                "type": "text",
                                                "text": item_dump.get("text", ""),
                                            }
                                        serializable_output.append(item_dump)
                                    else:
                                        serializable_output.append(str(item))
                            elif hasattr(tool_result_content, "model_dump"):
                                serializable_output = tool_result_content.model_dump(
                                    mode="json", exclude_none=True
                                )
                                if serializable_output.get("type") == "text":
                                    serializable_output = {
                                        "type": "text",
                                        "text": serializable_output.get("text", ""),
                                    }
                            elif (
                                isinstance(
                                    tool_result_content, (dict, int, float, bool)
                                )
                                or tool_result_content is None
                            ):
                                serializable_output = tool_result_content
                            else:
                                logger.warning(
                                    f"Tool result output for '{tool_name}' is of complex type {type(tool_result_content)}. Converting to string."
                                )
                                serializable_output = str(tool_result_content)

                            tool_result_data = {
                                "index": llm_event_original_index,
                                "tool_use_id": tool_id,
                                "tool_name": tool_name,
                                "status": "success",
                                "output": serializable_output,
                                "is_error": False,
                            }
                            yield {
                                "event_type": "tool_result",
                                "data": tool_result_data,
                            }
                        except json.JSONDecodeError as json_err:
                            logger.error(
                                f"Failed to parse tool input JSON for tool '{tool_name}': {json_err}"
                            )
                            tool_error_data = {
                                "index": llm_event_original_index,
                                "tool_use_id": tool_id,
                                "tool_name": tool_name,
                                "error_message": f"Invalid JSON input for tool: {str(json_err)}",
                            }
                            yield {
                                "event_type": "tool_execution_error",
                                "data": tool_error_data,
                            }
                        except Exception as e:
                            logger.error(
                                f"Error executing tool {tool_name} via stream: {e}",
                                exc_info=True,
                            )
                            tool_error_data = {
                                "index": llm_event_original_index,
                                "tool_use_id": tool_id,
                                "tool_name": tool_name,
                                "error_message": str(e),
                            }
                            yield {
                                "event_type": "tool_execution_error",
                                "data": tool_error_data,
                            }
                    elif (
                        llm_event_original_index is None
                        and event_data.get("content_type") == "tool_use"
                    ):
                        logger.warning(
                            f"Content_block_stop for tool_use event missing 'index'. Cannot process tool call. Data: {event_data}"
                        )

                elif event_type == "stream_end":
                    llm_call_stop_reason = event_data.get("stop_reason")
                    logger.info(
                        f"LLM stream call processing finished by ATP. LLM Stop Reason: {llm_call_stop_reason}"
                    )
                    yield {
                        "event_type": "llm_call_completed",
                        "data": {
                            "stop_reason": llm_call_stop_reason,
                            "original_event_data": event_data,
                        },
                    }
                    break

                else:  # Handles message_start, text_block_start, text_delta, message_delta, ping, error, unknown
                    yield {"event_type": event_type, "data": event_data}

        except Exception as e:
            logger.error(f"Error during agent turn streaming: {e}", exc_info=True)
            yield {
                "event_type": "error",
                "data": {"message": f"Agent turn processing error: {str(e)}"},
            }
        finally:
            logger.debug("Finished streaming conversation turn.")

    async def _process_tool_calls(
        self, llm_response: AgentOutputMessage
    ) -> List[MessageParam]:
        """Handles tool execution based on LLM response."""
        logger.debug("Processing tool calls...")
        tool_results_for_next_turn: List[MessageParam] = []
        self._tool_uses_this_turn = []  # Reset for this turn
        has_tool_calls = False

        if not llm_response.content:
            logger.warning(
                "LLM response has stop_reason 'tool_use' but no content blocks."
            )
            return []  # Return empty list, Agent loop should handle this unexpected state

        for block in llm_response.content:
            if block.type == "tool_use":
                has_tool_calls = True
                if block.id and block.name and block.input is not None:
                    # Record the tool use attempt
                    self._tool_uses_this_turn.append(
                        {
                            "id": block.id,
                            "name": block.name,
                            "input": block.input,
                        }
                    )
                    logger.info(
                        f"Executing tool '{block.name}' via host (ID: {block.id})"
                    )
                    try:
                        # Execute the tool via the host instance
                        tool_result_content = await self.host.execute_tool(
                            tool_name=block.name,
                            arguments=block.input,
                            agent_config=self.config,  # Pass agent config for filtering
                        )
                        logger.debug(f"Tool '{block.name}' executed successfully.")
                        # Create a result block using the host's tool manager helper
                        tool_result_block_data: Dict[str, Any] = (
                            self.host.tools.create_tool_result_blocks(
                                tool_use_id=block.id, tool_result=tool_result_content
                            )
                        )
                        message_with_tool_result: MessageParam = {
                            "role": "user",
                            "content": [
                                cast(ToolResultBlockParam, tool_result_block_data)
                            ],
                        }
                        tool_results_for_next_turn.append(message_with_tool_result)
                    except Exception as e:
                        # Handle tool execution errors
                        logger.error(
                            f"Error executing tool {block.name}: {e}", exc_info=True
                        )
                        error_content = f"Error executing tool '{block.name}': {str(e)}"
                        # Create an error result block
                        error_tool_result_block_data: Dict[str, Any] = (
                            self.host.tools.create_tool_result_blocks(
                                tool_use_id=block.id, tool_result=error_content
                            )
                        )
                        message_with_tool_error_result: MessageParam = {
                            "role": "user",
                            "content": [
                                cast(ToolResultBlockParam, error_tool_result_block_data)
                            ],
                        }
                        tool_results_for_next_turn.append(
                            message_with_tool_error_result
                        )
                else:
                    # Log if a tool_use block is missing required fields
                    logger.warning(
                        f"Skipping tool_use block with missing fields: {block.model_dump_json()}"
                    )

        if not has_tool_calls:
            # This case should ideally not be reached if stop_reason was 'tool_use',
            # but log it if it occurs.
            logger.warning(
                "LLM stop_reason was 'tool_use' but no valid tool_use blocks found in content."
            )

        logger.debug(
            f"Processed {len(self._tool_uses_this_turn)} tool calls, generated {len(tool_results_for_next_turn)} result blocks."
        )
        return tool_results_for_next_turn

    def _handle_final_response(
        self, llm_response: AgentOutputMessage
    ) -> Optional[AgentOutputMessage]:
        """
        Handles the final response, including schema validation.
        Returns the validated response if successful, or None if schema validation fails,
        signaling the need for a retry/correction message.
        """
        logger.debug("Handling final response...")

        # Extract text content
        text_content = None
        if llm_response.content:
            text_content = next(
                (
                    block.text
                    for block in llm_response.content
                    if block.type == "text" and block.text is not None
                ),
                None,
            )

        # If no text content, return the response as is (might be an error or unusual case)
        if not text_content:
            logger.warning("No text content found in final LLM response.")
            return llm_response

        # Perform schema validation if a schema is configured
        if self.config.config_validation_schema:  # Use renamed field
            logger.debug("Schema validation required.")
            try:
                json_content = json.loads(text_content)
                validate(
                    instance=json_content, schema=self.config.config_validation_schema
                )  # Use renamed field
                logger.debug("Response validated successfully against schema.")
                return (
                    llm_response  # Schema is valid, return the original response object
                )
            except json.JSONDecodeError:
                logger.warning(
                    "Final response was not valid JSON, schema validation failed."
                )
                return None  # Signal failure (Agent needs to send correction)
            except JsonSchemaValidationError as e:
                logger.warning(f"Schema validation failed: {e.message}")
                return None  # Signal failure (Agent needs to send correction)
            except Exception as e:
                logger.error(
                    f"Unexpected error during schema validation: {e}", exc_info=True
                )
                return None  # Signal failure on unexpected validation errors
        else:
            # No schema defined, response is considered final and valid
            logger.debug("No schema defined, skipping validation.")
            return llm_response
