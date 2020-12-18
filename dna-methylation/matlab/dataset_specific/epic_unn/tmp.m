if contains(m, 'p_value')
    res_tbl = sortrows(res_tbl, m, 'descend');
    values = -log10(res_tbl.(m));
    if strcmp(m, 'kw_p_value')
        xlab = '$-\log_{10}($Kruskal-Wallis p-value$)$';
    else
        spl = split(m, '_');
        group = spl(1);
        target = spl(2);
        tmp = sprintf('%s p-value for %s', target, group);
        xlab = sprintf('$-log_{10}($%s$)$', tmp);
    end
else
    res_tbl = sortrows(res_tbl, m, 'ascend');
    values = res_tbl.(m);
    
    spl = split(m, '_');
    group = spl(1);
    target = spl(2);
    xlab = sprintf('%s-Association $R^2$ for %s', target, group);
end