# Commands that are handy when working with ansible

### Wondering what hosts/variables ansible is finding?
`ansible-inventory -i hosts2.yml --graph --vars`

### Debug
This took me years to discover..

`- debug: var=variable_name`


