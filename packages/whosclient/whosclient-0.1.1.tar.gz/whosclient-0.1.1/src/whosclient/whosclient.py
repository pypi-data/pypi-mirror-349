import requests
from typing import List
import logging
from datetime import datetime

class OmOgcTimeseriesClient:

    url : str

    token : str

    timeseries_max : int

    timeseries_per_page : int

    view : str

    threshold_begin_date : str

    pagination_limit : int

    default_config : dict = {
        "url": 'https://gs-service-preproduction.geodab.eu/gs-service/services/essi', # 'https://whos.geodab.eu/gs-service/services/essi',
        "token": 'MY_TOKEN',
        "timeseries_max": 48000,
        "timeseries_per_page": 400,
        "view": 'whos-plata',
        "threshold_begin_date": None,
        "pagination_limit": 1000
    }

    def __init__(self, config : dict = None):
        for key, val in self.default_config.items():
            if config is not None and key in config:
               setattr(self, key, config[key])
            else:
               setattr(self, key, val)

    def getTimeseriesWithPagination(
            self,
            **kwargs
    ):
        members = []
        is_last = False
        resumption_token = None
        while not is_last:
            result = self.getTimeseries(**kwargs, resumptionToken=resumption_token)
            if "member" not in result:
                is_last = True
            else:
                members.extend(result["member"])
                if result["completed"]:
                    is_last = True
                else:
                    resumption_token = result["resumptionToken"]
        return {
            "member": members
        }

    def getTimeseries(
            self,
            feature : str = None,
            observationIdentifier : str = None,
            beginPosition : str = None,
            endPosition : str = None,
            limit : int = None,
            offset : int = None,
            useCache : bool = False,
            view : str = None,
            has_data : bool = False,
            profiler : str = "om-api",
            resumptionToken : str = None,
            west : float = None, 
            south : float = None, 
            east : float = None, 
            north : float = None,
            ontology : str = None,
            observedProperty : str = None,
            timeInterpolation : str = None,
            intendedObservationSpacing : str = None,
            aggregationDuration : str = None,
            includeData : bool = None,
            asynchDownload : bool = None,
            format : str = None) -> dict:

        profiler_path =  "timeseries-api/timeseries" if profiler == "timeseries-api" else "om-api/observations"        
        view = view if view is not None else self.view
        limit = limit if limit is not None else self.pagination_limit
        url = "%s/token/%s/view/%s/%s" % (self.url, self.token, view, profiler_path)
        logging.debug("url: %s" % url)
        params = {
                "monitoringPoint": feature,
                "timeseriesIdentifier": observationIdentifier,
                "beginPosition": beginPosition,
                "endPosition": endPosition,
                "limit": limit,
                "offset": offset,
                "useCache": useCache
            } if profiler == "timeseries-api" else {
                "feature": feature,
                "observationIdentifier": observationIdentifier,
                "beginPosition": beginPosition,
                "endPosition": endPosition,
                "east": east,
                "south": south,
                "west": west,
                "north": north,
                "observedProperty": observedProperty,
                "ontology": ontology,
                "timeInterpolation": timeInterpolation,
                "intendedObservationSpacing": intendedObservationSpacing,
                "aggregationDuration": aggregationDuration,
                "includeData": includeData,
                "asynchDownload": asynchDownload,
                "useCache": useCache,
                "limit": limit,
                "useCache": useCache,
                "resumptionToken": resumptionToken,
                "format": format
            } 
        response = requests.get(
            url,
            params)
        if response.status_code != 200:
            raise ValueError("request failed, status code: %s, message: %s" % (response.status_code, response.text))
        result = response.json()
        if has_data and "member" in result:
            result["member"] = self.filterByAvailability(result["member"],self.threshold_begin_date)
        return result

    def filterByAvailability(
            self,
            members : list,
            threshold_begin_date : str = None) -> list:
        if threshold_begin_date is not None:
            return [x for x in members if "phenomenonTime" in x and datetime.fromisoformat(x["phenomenonTime"]["end"]) >=  datetime.fromisoformat(threshold_begin_date)]
        else:
            return [x for x in members if "phenomenonTime" in x]

    def getData(
        self,
        beginPosition : str,
        endPosition : str,
        feature : str = None,
        observedProperty : str = None,
        observationIdentifier : str = None,
        view : str = None,
        timeInterpolation : str = None, # MAX, MIN, TOTAL, AVERAGE, MAX_PREC, MAX_SUCC, CONTINUOUS, ...
        intendedObservationSpacing : str = None, # ISO8601 i.e. P1D
        aggregationDuration : str = None, # ISO8601 i.e. P1D
        ontology : str = None,
        profiler : str = "om-api"
    ) -> List[dict]:        
        if observationIdentifier is None:
            if feature is None:
                raise TypeError("feature can't be None if timeseriesIdentifier is None")
            if observedProperty is None:
                raise TypeError("observedProperty can't be None if timeseriesIdentifier is None")
        view = view if view is not None else self.view
        
        # First, retrieves timeseries metadata for the monitoring point or timeseriesIdentifier
        if observationIdentifier is None:
            ts_metadata = self.getTimeseries(
                view = view, 
                feature = feature,
                observedProperty = observedProperty,
                timeInterpolation = timeInterpolation,
                intendedObservationSpacing = intendedObservationSpacing,
                aggregationDuration = aggregationDuration,
                ontology = ontology,
                profiler = profiler
            )
            if not len(ts_metadata["member"]):
                raise FileNotFoundError("Observations not found for  monitoringPoint: %s, observedProperty: %s" % (feature, observedProperty))
            if profiler == "timeseries-api":
                ts_matches = [x for x in ts_metadata["member"] if x["observedProperty"]["href"] == observedProperty]
                if len(ts_matches):
                    observationIdentifier = ts_matches[0]["id"]
                else:
                    raise FileNotFoundError("timeseries metadata not found for monitoringPoint: %s, observedProperty: %s" % (feature, observedProperty))
            else:
                if len(ts_metadata["member"]) > 1:
                    logging.warning("Matched %i observations, retrieving first match" % len(ts_metadata["member"]))
                observationIdentifier = ts_metadata["member"][0]["id"]
        else: 
            ts_metadata = self.getTimeseries(
                view = view,
                observationIdentifier = observationIdentifier,
                profiler = profiler
            )
            if not len(ts_metadata):
                raise ValueError("observation metadata not found for observationIdentifier: %s" % observationIdentifier)
            
        # Now that we have the timeseries identifier, retrieve data
        ts_data = self.getTimeseries(
            view = view,
            beginPosition = beginPosition,
            endPosition = endPosition,
            observationIdentifier = observationIdentifier,
            includeData = True,
            profiler = profiler
        )
        return [ 
            {
                "date": p["time"]["instant"],
                "value": p["value"]
            }
            for p in ts_data["member"][0]["result"]["points"]
        ]
