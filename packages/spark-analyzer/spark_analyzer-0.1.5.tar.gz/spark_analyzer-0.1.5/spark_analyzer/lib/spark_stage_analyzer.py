from .api_client import APIClient
import json
import logging
import requests
from typing import Optional, Dict, Any, List, Tuple, Set
from enum import Enum
import datetime
import traceback

class StorageFormat(Enum):
    HUDI = "hudi"
    ICEBERG = "iceberg"
    DELTA = "delta"
    PARQUET = "parquet"
    UNKNOWN = "unknown"

class StageType(Enum):
    EXTRACT = "extract"
    TRANSFORM = "transform"
    LOAD = "load"
    UNKNOWN = "unknown"

class SparkStageAnalyzer:
    def __init__(self, api_client: APIClient):
        self.api_client = api_client
        self._load_keywords()
        self.opt_out_fields = set()
        logging.debug("Initialized SparkStageAnalyzer")

    def _load_keywords(self):
        """Load keywords for different storage formats and operations"""
        self.hoodie_keywords = self.api_client.hoodie_keywords
        
        for category, keywords in self.hoodie_keywords.items():
            if isinstance(keywords, list):
                logging.debug(f"Loaded {len(keywords)} keywords for category: {category}")

    def set_opt_out_fields(self, fields: Set[str]):
        """Set which fields should be excluded from output (hashed or omitted)"""
        if not isinstance(fields, set):
            logging.warning(f"opt_out_fields should be a set, got {type(fields)}. Converting to set.")
            fields = set(fields)
            
        self.opt_out_fields = fields
        logging.debug(f"Set opt-out fields: {fields}")

    def format_stage_for_proto(self, stage: Dict[str, Any], app_id: str, executor_metrics: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Format a stage's data according to the proto structure."""
        try:
            stage_id = stage.get("stageId")
            if stage_id is None:
                logging.warning("Found stage with missing stageId, skipping")
                return None
                
            logging.debug(f"Processing stage {stage_id} for application {app_id}")
                
            try:
                stage_details = self.api_client.get_stage_details_with_tasks(app_id, stage_id)
                if not stage_details:
                    logging.debug(f"No stage details found for stage {stage_id}")
                    return None
            except Exception as e:
                logging.error(f"Error fetching details for stage {stage_id}: {str(e)}")
                raise ValueError(f"Failed to get stage details: {str(e)}")

            stage_attempt = stage_details[0] if isinstance(stage_details, list) else stage_details
            
            tasks = stage_attempt.get("tasks", {})
            num_tasks = len(tasks)
            logging.debug(f"Stage {stage_id} has {num_tasks} tasks")
            
            try:
                total_executor_count = len([e for e in executor_metrics if e["id"] != "driver"])
                executors, cores, task_executor_ids = self._get_executors_for_stage(
                    stage_attempt, 
                    executor_metrics,
                    total_executors=total_executor_count
                )
                executor_ids = [executor["id"] for executor in executors]
                logging.debug(f"Found {len(executor_ids)} executors for stage {stage_id}")
                
                if len(executor_ids) == 0 and len(task_executor_ids) > 0:
                    logging.info(f"Using {len(task_executor_ids)} task executor IDs for stage {stage_id} instead of metrics")
                    executor_ids = list(task_executor_ids)
            except Exception as e:
                logging.error(f"Error determining executors for stage {stage_id}: {str(e)}")
                logging.debug(f"Exception traceback: {traceback.format_exc()}")
                executor_ids = []
                
            name = stage.get("name", "")
            description = stage.get("description", "")
            details = stage.get("details", "")

            if "name" in self.opt_out_fields:
                logging.debug(f"Hashing stage name for privacy (stage {stage_id})")
                name = f"name_hash_{hash(name)}"
            if "description" in self.opt_out_fields:
                logging.debug(f"Hashing stage description for privacy (stage {stage_id})")
                description = f"description_hash_{hash(description)}"
            if "details" in self.opt_out_fields:
                logging.debug(f"Hashing stage details for privacy (stage {stage_id})")
                details = f"details_hash_{hash(details)}"

            submission_time = stage_attempt.get("submissionTime", "")
            completion_time = stage_attempt.get("completionTime", "")
            
            stage_duration_ms = 0
            if submission_time and completion_time:
                try:
                    submission_dt = datetime.datetime.strptime(submission_time.split("GMT")[0], "%Y-%m-%dT%H:%M:%S.%f")
                    completion_dt = datetime.datetime.strptime(completion_time.split("GMT")[0], "%Y-%m-%dT%H:%M:%S.%f")
                    stage_duration_ms = int((completion_dt - submission_dt).total_seconds() * 1000)
                    logging.debug(f"Stage {stage_id} duration: {stage_duration_ms} ms")
                except Exception as e:
                    logging.error(f"Error calculating duration for stage {stage_id}: {str(e)}")
                    logging.debug(f"Submission time: {submission_time}")
                    logging.debug(f"Completion time: {completion_time}")
                    logging.debug(f"Error details: {traceback.format_exc()}")
                    
            executor_run_time_ms = stage_attempt.get("executorRunTime", 0)
            
            try:
                workflow_info = self._get_workflow_info(name, description, stage_id, app_id)
                logging.debug(f"Stage {stage_id} workflow type: {workflow_info['type']}, storage format: {workflow_info['storage_format']}")
            except Exception as e:
                logging.error(f"Error determining workflow info for stage {stage_id}: {str(e)}")
                logging.debug(f"Exception traceback: {traceback.format_exc()}")
                workflow_info = {
                    "type": "UNKNOWN",
                    "storage_format": "STORAGE_UNKNOWN",
                    "custom_info": ""
                }

            stage_data = {
                "stage_id": stage_id,
                "application_id": app_id,
                "stage_name": name,
                "stage_description": description,
                "stage_details": details,
                "num_tasks": num_tasks,
                "num_executors_used": len(executor_ids),
                "executor_ids": executor_ids,
                "submission_time": submission_time,
                "completion_time": completion_time,
                "executor_run_time_ms": executor_run_time_ms,
                "stage_duration_ms": stage_duration_ms,
                "workflow_info": workflow_info
            }
            
            logging.debug(f"Successfully processed stage {stage_id}")
            return stage_data
            
        except Exception as e:
            stage_id = stage.get('stageId', 'unknown')
            logging.error(f"Error formatting stage {stage_id}: {str(e)}")
            logging.debug(f"Exception traceback: {traceback.format_exc()}")
            return None

    def _count_keyword_occurrences(self, text: str) -> Dict[str, int]:
        counts = {
            "EXTRACT": 0,
            "TRANSFORM": 0,
            "LOAD": 0,
            "JOIN": 0,
            "INDEXING": 0,
            "HUDI_METADATA": 0
        }
        
        for keyword in self.hoodie_keywords.get("scan_keywords", []):
            if keyword.lower() in text:
                counts["EXTRACT"] += 1
                
        for keyword in self.hoodie_keywords.get("transform_keywords", []):
            if keyword.lower() in text:
                counts["TRANSFORM"] += 1
                
        for keyword in self.hoodie_keywords.get("merge_write", []):
            if keyword.lower() in text:
                counts["LOAD"] += 1
        for keyword in self.hoodie_keywords.get("insert_write", []):
            if keyword.lower() in text:
                counts["LOAD"] += 1
                
        for keyword in self.hoodie_keywords.get("join_keywords", []):
            if keyword.lower() in text:
                counts["JOIN"] += 1
                
        for keyword in self.hoodie_keywords.get("indexing_keywords", []):
            if keyword.lower() in text:
                counts["INDEXING"] += 1
                
        for keyword in self.hoodie_keywords.get("hudi_metadata_keywords", []):
            if keyword.lower() in text:
                counts["HUDI_METADATA"] += 1
                
        return counts

    def _get_workflow_info(self, stage_name: str, stage_description: str, stage_id: str = None, app_id: str = None) -> Dict[str, Any]:
        """Determine workflow type and storage format for a stage using frequency-based classification."""
        storage_format = self._determine_storage_format(stage_name, stage_description)
        text = f"{stage_name} {stage_description}".lower()
        
        if app_id and stage_id:
            try:
                stage_obj = self.api_client.get_stage(app_id, stage_id)
                if isinstance(stage_obj, list) and stage_obj:
                    stage_obj = stage_obj[0]
                if stage_obj and self.api_client.is_indexing_candidate(stage_obj):
                    return {
                        "type": "INDEXING",
                        "storage_format": self._get_storage_format_proto(storage_format),
                        "custom_info": "record_level_indexing"
                    }
            except Exception as e:
                logging.debug(f"Could not determine if stage {stage_id} is indexing candidate: {str(e)}")
        
        keyword_counts = self._count_keyword_occurrences(text)
        logging.debug(f"Stage {stage_id} keyword counts: {keyword_counts}")
        
        max_count = 0
        workflow_type = "UNKNOWN"
        custom_info = ""
        
        priority_order = ["INDEXING", "HUDI_METADATA", "JOIN", "LOAD", "TRANSFORM", "EXTRACT"]
        
        for category in priority_order:
            if keyword_counts[category] > max_count:
                max_count = keyword_counts[category]
                workflow_type = category
        
        if workflow_type == "JOIN":
            if "broadcast" in text:
                custom_info = "broadcast_join"
                logging.debug(f"Stage {stage_id} identified as broadcast join")
            elif "shuffle" in text:
                custom_info = "shuffle_join"
                logging.debug(f"Stage {stage_id} identified as shuffle join")
        
        return {
            "type": workflow_type,
            "storage_format": self._get_storage_format_proto(storage_format),
            "custom_info": custom_info
        }
        
    def _get_storage_format_proto(self, storage_format: StorageFormat) -> str:
        storage_format_map = {
            StorageFormat.HUDI: "HUDI",
            StorageFormat.ICEBERG: "ICEBERG",
            StorageFormat.DELTA: "DELTA",
            StorageFormat.PARQUET: "PARQUET",
            StorageFormat.UNKNOWN: "STORAGE_UNKNOWN"
        }
        return storage_format_map.get(storage_format, "STORAGE_UNKNOWN")

    def _get_executors_for_stage(self, stage_details: Dict[str, Any], executor_metrics: List[Dict[str, Any]], total_executors: Optional[int] = None) -> Tuple[List[Dict[str, Any]], int, set]:
        """Get executors used for a specific stage."""
        stage_id = stage_details.get('stageId', 'unknown')
        task_data = stage_details.get("tasks", {})
        
        if not task_data:
            logging.debug(f"No task data found for stage {stage_id}. This is normal for stages that are queued, just starting, or already completed.")
            return [], 0, set()
        
        task_executor_ids = set()
        for task_id, task in task_data.items():
            executor_id = task.get("executorId")
            if executor_id:
                task_executor_ids.add(executor_id)
        
        if not task_executor_ids:
            logging.debug(f"No executor IDs found in tasks for stage {stage_id}. Tasks may be pending assignment to executors.")
            return [], 0, set()
            
        logging.debug(f"Found {len(task_executor_ids)} unique executor IDs in tasks for stage {stage_id}")
        
        found_executors = []
        total_cores = 0
        
        if not executor_metrics:
            logging.debug(f"No executor metrics available. Using task executor IDs only for stage {stage_id}.")
            return [], 0, task_executor_ids
        
        for executor in executor_metrics:
            executor_id = executor.get("id")
            if executor_id in task_executor_ids:
                found_executors.append(executor)
                total_cores += executor.get("totalCores", 0)
                
                if len(found_executors) == len(task_executor_ids):
                    logging.debug(f"Found all {len(task_executor_ids)} executors in metrics for stage {stage_id}")
                    break
                    
                if total_executors is not None and len(found_executors) == total_executors:
                    logging.debug(f"Found all {total_executors} total executors for stage {stage_id}")
                    break
        
        if task_executor_ids and found_executors:
            if len(found_executors) < len(task_executor_ids):
                logging.debug(f"Found only {len(found_executors)}/{len(task_executor_ids)} executors in metrics for stage {stage_id}. Some executors may have been reused or removed.")
        
        logging.debug(f"Found {len(found_executors)} executors with {total_cores} total cores for stage {stage_id}")
        
        return found_executors, total_cores, task_executor_ids

    def _determine_storage_format(self, stage_name: str, stage_description: str) -> StorageFormat:
        """Determine the storage format for a stage."""
        combined_text = f"{stage_name} {stage_description}".lower()
        
        if any(identifier in combined_text for identifier in self.hoodie_keywords.get("hoodie_identifiers", [])):
            return StorageFormat.HUDI
        elif "iceberg" in combined_text:
            return StorageFormat.ICEBERG
        elif "delta" in combined_text:
            return StorageFormat.DELTA
        elif "parquet" in combined_text:
            return StorageFormat.PARQUET
        else:
            return StorageFormat.UNKNOWN
    
    def _determine_stage_type(
        self,
        storage_format: StorageFormat,
        stage_name: str,
        stage_description: str
    ) -> StageType:
        """Determine the type of stage (EXTRACT, TRANSFORM, LOAD)."""
        if storage_format == StorageFormat.HUDI:
            return self._analyze_hudi_stage(stage_name, stage_description)
        
        return self._analyze_generic_stage(stage_name, stage_description)
    
    def _analyze_hudi_stage(
        self,
        stage_name: str,
        stage_description: str
    ) -> StageType:
        """Analyze Hudi specific stage using keywords"""
        text = f"{stage_name} {stage_description}".lower()
        
        # Check for extract operations
        if any(keyword in text for keyword in self.hoodie_keywords["scan_keywords"]):
            return StageType.EXTRACT
            
        # Check for transform operations
        if any(keyword in text for keyword in self.hoodie_keywords["transform_keywords"]):
            return StageType.TRANSFORM
            
        # Check for load operations (merge_write or insert_write)
        if (any(keyword in text for keyword in self.hoodie_keywords.get("merge_write", [])) or
            any(keyword in text for keyword in self.hoodie_keywords.get("insert_write", []))):
            return StageType.LOAD

        return StageType.UNKNOWN

    def _analyze_generic_stage(
        self,
        stage_name: str,
        stage_description: str
    ) -> StageType:
        """Analyze generic (non-format-specific) stage using keywords"""
        text = f"{stage_name} {stage_description}".lower()
        
        # Use generic keywords for ETL classification
        if any(keyword in text for keyword in self.hoodie_keywords["scan_keywords"]):
            return StageType.EXTRACT
            
        if any(keyword in text for keyword in self.hoodie_keywords["transform_keywords"]):
            return StageType.TRANSFORM
            
        # Check for load operations (merge_write or insert_write)
        if (any(keyword in text for keyword in self.hoodie_keywords.get("merge_write", [])) or
            any(keyword in text for keyword in self.hoodie_keywords.get("insert_write", []))):
            return StageType.LOAD
            
        return StageType.UNKNOWN 