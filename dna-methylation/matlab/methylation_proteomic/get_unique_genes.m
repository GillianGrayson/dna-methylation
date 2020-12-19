function unique_genes = get_unique_genes(genes_raw, delimeters)

genes = {};
num_cells = size(genes_raw, 1);
for gene_row_id = 1:num_cells
    genes_row = genes_raw{gene_row_id};
    cells_genes = strsplit(genes_row, delimeters);
    for gene = cells_genes
        if ~strcmp(gene, '')
            genes = vertcat(genes, gene);
        end
    end
end
unique_genes = unique(genes);

end