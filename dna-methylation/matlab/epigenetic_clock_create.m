figures_path = sprintf('%s/figures/clock/dataType(%s)_norm(%s)_part(%s)', dataset_path, data_type, norm, part);
if ~exist(figures_path, 'dir')
    mkdir(figures_path)
end

estimation = 'age';

cgs = importdata('epigenetic_clock.txt');

t = obs;
for cg_id = 1:size(cgs)
    cg = cgs{cg_id};
    cg_data = betas{cg, :}';
    t{:, cg} = cg_data;
end

formula = strjoin(cgs,'+');
lm = fitlm(t, sprintf('%s~%s', estimation, formula));

yfit = predict(lm, t);
ae = abs(yfit - t.(estimation));
R2 = lm.Rsquared.Ordinary
RMSE = lm.RMSE
mae = mean(ae)

save epigenetic_clock lm;