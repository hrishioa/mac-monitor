echo "$(gdate +%s.%N), $(istats battery temp --no-scale --value-only),
$(istats cpu --no-scale --value-only), $(istats battery charge --no-scale
--value-only), $(istats battery remain --no-scale --value-only), $(brightness
-l | pcregrep -o1 '[\s\S]+(\d+?\.\d+)$')" >>
/Users/hebe/HebeVestigations/stats2.csv
