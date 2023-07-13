TrackProjectId.py
==================================

This example event plugin script hooks into the "OnJobSubmitted" callback and allows a studio to globally extract the first 5 characters for each submitted job's job name and add it to the first Extra Info column known as: "Extra Info 0 "; which can be renamed to something logical for studio specific display purposes and also to allow a customer to generate a report/graph against later completed Deadline jobs via the Deadline Stats module.
