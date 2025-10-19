function mean_lv_uptake = get_mean_lv_uptake(rec_base, lv_template)
  tx_lv_seg = lv_template>0;
  mean_lv_uptake = sum(rec_base.*tx_lv_seg, 'all') / sum(tx_lv_seg(:));
end