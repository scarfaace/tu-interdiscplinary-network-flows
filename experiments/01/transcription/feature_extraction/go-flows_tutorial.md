Here you have an example of how to call/execute go-flows:

`./go-flows run features config.json export csv output.csv source libpcap input.pcap`

where "input.pcap" is the traffic capture from which you want to extract features. "output.csv" is the output csv file in which you will store your preprocessed, vector-structured data, and "config.json" is the file in which you tell go-flows how to extract features.

Attached an example of a "config.json" file that extracts features according to a popular format. In the paper you cited you can find more information and sources about such format and the used variation. I comment briefly on 5 different parts of the json file:

- "flows": [{...}]
  
This is the features that you want to extract from your flows. There are infinite possibilities and combinations, but you can find many basic features and their description here: https://www.iana.org/assignments/ipfix/ipfix.xhtml

- "active_timeout": ...,

This is the maximum time that you observe a flow. If the flow is longer, a new flow will be formed. Between 20 seconds and 1 minute could be a starting option. It could be longer, but it has some effect on the computational requirements and in the granularity of your analysis. But it could be justify. For example, I'm currently working on an application that I used a 2-days timeout.

- "idle_timeout": ...,

This is the maximum time that you allow a flow to be passive (no communication)

- "bidirectional": ...,

If your flows are defined in one direction (A->B) or in both directions (A<->B)

- "key_features": [...]

This is the flow definition, kinda mask. It can be 2-tuple, 4-tuple, 5-tuple, or whatever you like. If, for example, you define a 2-tuple key ("sourceIPAddress", "destinationIPAddress"), everything (I mean: packets) that shows the same values in these two fields will be considered belonging to the same flow (also within the scope covered by the active and idle timeouts).


> One more thing - I thought that it may be a reasonable choice to compare the performance of the model above the NTFT data with the multi-key vector data from this paper. Does that make sense in your opinion? I see that you focused on encrypted communication there and did some research around this multi-key vector.

Perhaps, but it is too soon for that. As far as I see (well, I haven't seen any results or documents from you yet), you are still in step 1. Such comparisons are rather Alex's stuff. In your case, I would consider less sophisticated formats for the comparison, but it's up to you.

> Possibly, do you have a JSON for the `features` argument of go-flows for the multi-key vectors extraction? In the section V. Experiments, you state that you used go-flows to extract information from pcap files and formed multi-key vectors. So maybe this would help me and I do not need to build that on my own.
You cannot directly extract the multi-key vector with go-flows. The multi-key approach is a bit more complicated. You need to extract different vector formats first and later merge them together with additional scripts. This is described here:

https://github.com/CN-TU/multi-key-vector-experiments

Once you extracted the multi-key vectors with go-flows, how did you label the data, please? Maybe do you have some scripts for that so I do not have to build it again on my own?
Fares created some scripts for the CIC2017IDS dataset. They are also provided in the github repo above. You can contact him is you have doubts in this respect.