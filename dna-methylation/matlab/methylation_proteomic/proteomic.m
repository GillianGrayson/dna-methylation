clear all;

dataPath = sprintf('E:/YandexDisk/Work/pydnameth/methylation_and_proteomic');
proteomicPath = sprintf('%s/proteomic_data', dataPath);
methylationPath = sprintf('%s/limma', dataPath);

figuresPath = sprintf('%s/figures', dataPath);
if ~exist(figuresPath, 'dir')
    mkdir(figuresPath)
end

gtex_fn =  sprintf('%s/GTEx.xlsx', dataPath);
opts = detectImportOptions(gtex_fn);
gtex = readtable(gtex_fn, opts);
[unique_rows, ids] = unique(gtex.('Description'));
ids = sort(ids);
gtex = gtex(ids, :);
gtex.Properties.RowNames = gtex.('Description');

blood_SS_genes = importdata(sprintf('%s/GSE87571/Sex/genes_betas_Sex_logFC(2.50e-02)_Sex_P_Value_fdr_bh(1.00e-03).csv', methylationPath));
blood_AA_genes = importdata(sprintf('%s/GSE87571/Age/genes_betas_Age_logFC(1.50e-03)_Age_P_Value_fdr_bh(1.00e-03).csv', methylationPath));
blood_SSAA_genes = intersect(blood_SS_genes, blood_AA_genes);

brain_SS_genes = importdata(sprintf('%s/GSE74193/Sex/genes_betas_Sex_logFC(2.50e-02)_Sex_P_Value_fdr_bh(1.00e-03).csv', methylationPath));
brain_AA_genes = importdata(sprintf('%s/GSE74193/Age/genes_betas_Age_logFC(4.00e-03)_Age_P_Value_fdr_bh(1.00e-03).csv', methylationPath));
brain_SSAA_genes = intersect(brain_SS_genes, brain_AA_genes);

t1_fn = sprintf('%s/T1.xlsx', proteomicPath);
opts = detectImportOptions(t1_fn);
t1 = readtable(t1_fn, opts);
t1.Properties.RowNames = t1.('ID');
t4_fn = sprintf('%s/T4.xlsx', proteomicPath);
opts = detectImportOptions(t4_fn);
t4 = readtable(t4_fn, opts);
t4.Properties.RowNames = t4.('ID');
tbl = innerjoin(t1, t4, 'Keys','ID');
SS = tbl(tbl.('q_Sex') < 0.05, :);
AA = tbl(tbl.('q_Age') < 0.05, :);
SSAA = tbl(tbl.('q_Sex') < 0.05 & tbl.('q_Age') < 0.05, :);
proteomics_SS_genes = get_unique_genes(SS.('EntrezGeneSymbol'), {';', '.'});
proteomics_AA_genes = get_unique_genes(AA.('EntrezGeneSymbol'), {';', '.'});
proteomics_SSAA_genes = get_unique_genes(SSAA.('EntrezGeneSymbol'), {';', '.'});

figuresPathLocal = sprintf('%s/figures/SS', dataPath);
if ~exist(figuresPathLocal, 'dir')
    mkdir(figuresPathLocal)
end
fig = plot_gtex_expDiff({blood_SS_genes, brain_SS_genes, proteomics_SS_genes}, gtex, {'GSE87571', 'GSE74193', 'Proteomic'}, figuresPathLocal, 0, 'Sex-Specific');
title('Sex-Specific', 'FontSize', 30, 'FontWeight', 'normal', 'Interpreter', 'latex');
fn_fig = sprintf('%s/KW_vertical_SexSpecific', figuresPath);
oqs_save_fig(fig, fn_fig);

figuresPathLocal = sprintf('%s/figures/AA', dataPath);
if ~exist(figuresPathLocal, 'dir')
    mkdir(figuresPathLocal)
end
fig = plot_gtex_expDiff({blood_AA_genes, brain_AA_genes, proteomics_AA_genes}, gtex, {'GSE87571', 'GSE74193', 'Proteomic'}, figuresPathLocal, 0, 'Age-Associated');
title('Age-Associated', 'FontSize', 30, 'FontWeight', 'normal', 'Interpreter', 'latex');
fn_fig = sprintf('%s/KW_vertical_AgeAssociated', figuresPath);
oqs_save_fig(fig, fn_fig);

figuresPathLocal = sprintf('%s/figures/SSAA', dataPath);
if ~exist(figuresPathLocal, 'dir')
    mkdir(figuresPathLocal)
end
fig = plot_gtex_expDiff({blood_SSAA_genes, brain_SSAA_genes, proteomics_SSAA_genes}, gtex, {'GSE87571', 'GSE74193', 'Proteomic'}, figuresPathLocal, 0, 'Sex-Specific Age-Associated');
title('Sex-Specific Age-Associated', 'FontSize', 30, 'FontWeight', 'normal', 'Interpreter', 'latex');
fn_fig = sprintf('%s/KW_vertical_SexSpecificAgeAssociated', figuresPath);
oqs_save_fig(fig, fn_fig);

fig = plot_venn3({blood_SS_genes, brain_SS_genes, proteomics_SS_genes}, {'GSE87571', 'GSE74193', 'Proteomic'});
title('Sex-Specific', 'FontSize', 30, 'FontWeight', 'normal', 'Interpreter', 'latex');
fn_fig = sprintf('%s/venn_SexSpecific', figuresPath);
oqs_save_fig(fig, fn_fig);

fig = plot_venn3({blood_AA_genes, brain_AA_genes, proteomics_AA_genes}, {'GSE87571', 'GSE74193', 'Proteomic'});
title('Age-Associated', 'FontSize', 30, 'FontWeight', 'normal', 'Interpreter', 'latex');
fn_fig = sprintf('%s/venn_AgeAssociated', figuresPath);
oqs_save_fig(fig, fn_fig);

fig = plot_venn3({blood_SSAA_genes, brain_SSAA_genes, proteomics_SSAA_genes}, {'GSE87571', 'GSE74193', 'Proteomic'});
title('Sex-Specific Age-Associated', 'FontSize', 30, 'FontWeight', 'normal', 'Interpreter', 'latex');
fn_fig = sprintf('%s/venn_SexSpecificAgeAssociated', figuresPath);
oqs_save_fig(fig, fn_fig);


