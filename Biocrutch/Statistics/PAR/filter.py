#!/usr/bin/env python3
__author__ = 'tomarovsky'
'''
Class for determining the coordinates of the pseudoautosomal region.
'''
from Biocrutch.Statistics.coverage_statistics.CoverageMetrics import CoveragesMetrics
from Biocrutch.Statistics.PAR.coordinator import Coordinator

class Filter:
    @staticmethod
    def concat_by_distanse(coordinates: list, min_region_length: int) -> list:
        """
        input list [[start, stop], [start, stop]]
        merge coordinates that are less than the specified distance
        """
        result = []
        start_flag = True
        for lst in range(len(coordinates)):
            if not result:
                result.append(coordinates[lst])
                continue
            d_first = coordinates[lst - 1][1]
            d_second = coordinates[lst][0]
            distance = d_second - d_first
            if distance > min_region_length:
                result.append(coordinates[lst])
            else:
                if start_flag:
                    start = coordinates[lst - 1][0]
                    start_flag = False
                stop = coordinates[lst][1]
                if result[-1][1] < start:
                    result.append([start, stop])
                    start_flag = True
                else:
                    del result[-1][-1]
                    result[-1].append(stop)
        return result


    @staticmethod
    def concat_by_median(coordinates: list, median_list: list, minimum_coverage, maximum_coverage) -> list:
        """
        merge coordinates if the area between them is with a suitable median
        """
        draft_result = []
        result= []
        median_flag = True
        median_index = 0
        start = None
        stop = None
        for lst in range(1, len(coordinates)):
            if median_list[median_index] >= minimum_coverage: # and median_list[median_index] < maximum_coverage:
                if median_flag:
                    start = coordinates[lst - 1][0]
                    median_flag = False
                stop = coordinates[lst][1]
            else:
                if start is not None and stop is not None:
                    draft_result.append([start, stop])
                median_flag = True
            median_index += 1
        if not draft_result:
            draft_result.append([start, stop])
            return draft_result
        elif draft_result[-1] != [start, stop]:
            draft_result.append([start, stop])
        [result.append(i) for i in draft_result if i not in result]
        return result

