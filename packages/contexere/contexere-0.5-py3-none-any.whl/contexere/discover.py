"""
Discover files following the naming convention
"""

import logging
import pandas as pd
from pathlib import Path

from contexere import __pattern__ as pattern


# Function to group files by common project and date
def build_context(directory='.', project_filter=None):
    context = dict()
    timeline = dict()

    # Iterate over files and directories in the specified folder
    for path in Path(directory).iterdir():
        match = pattern.match(path.name)
        if match:
            project = match.group('project')
            date = match.group('date')
            step = match.group('step')
            if project_filter is None or project == project_filter:
                if not project in context:
                    context[project] = dict()
                if not (date, step) in context[project]:
                    context[project][(date, step)] = list()
                if not (date + step) in timeline:
                    timeline[date + step] = dict()
                if not project in timeline[date + step]:
                    timeline[date + step][project] = list()
                context[project][(date, step)].append(path)
                timeline[date + step][project].append(path)
    return context, timeline
    
def last(timeline):
    events = list(timeline.keys())
    events.sort()
    latest = events[-1]
    return [project + latest for project in timeline[latest]]

def summary(directory='.'):
    context, timeline = build_context(directory)
    summary = pd.Series({project: len(context[project])
                         for project in context}).sort_values(ascending=False)

    if len(summary) == 0:
        raise ValueError('No context found in folder "{}".'.format(str(directory)))
    tail = last(timeline)
    artefacts = 'artefact' if len(tail) == 1 else 'artefacts'

    print(f"Summary of {'artefact' if len(summary) == 1 else 'artefacts'}:")
    print(summary)
    print(f"Last {'artefact' if len(tail) == 1 else 'artefacts'}: ", ', '.join(tail))

if __name__ == "__main__":
    summary()