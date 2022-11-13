# Stocks!

1. edit .env.dev-sample and save as .env.dev
2. docker-compose up -d --build
3. visit localhost:8000/graphql/ to use the api

## Sample queries

```
query Stock {
  allStockgraphenenode{
    edges{
      node{
        symbol
        name
      }
    }
  }
}
```

```
query Stock {
  allStockgraphenenode(name_Icontains: "INDUSTRIES") {
    edges {
      node {
        name
        symbol
      }
    }
  }
}
```

```
query Stock {
  allStockgraphenenode(symbol: "MLR") {
    edges {
      node {
        name
        symbol
      }
    }
  }
}
```

## Sample portfolio mutations

```
mutation Create {
  createPortfolio(
    input: {name: "My portfolio", description: "A good description", initialAccountBalance: 1000}
  ) {
    portfolio {
      name
      portfolioId
    }
  }
}
```

```
mutation Update {
  updatePortfolio(input: {id: 1, name: "New name", description: "New description"}) {
    portfolio {
      portfolioId
      name
      description
      initialAccountBalance
    }
  }
}
```

## Sample trade mutations

```
mutation Buy {
 buyStock(input:{portfolio:1,stock:11, price:10, volume:10})
  {
    trade{
      tradeId
      portfolio{name}
      stock{symbol}
      price
      volume
      tradeType
    }
    errors{
      field
      messages
    }
	}
}
```

```
mutation Sell {
 sellStock(input:{portfolio:1,stock:11, price:20, volume:5})
  {
    trade{
      tradeId
      portfolio{name}
      stock{symbol}
      price
      volume
      tradeType
    }
    errors{
      field
      messages
    }
	}
}
```

## Sample Errors

```
mutation CreateWithError {
  createPortfolio(
    input: {name: "My portfolio", description: "A good description", initialAccountBalance: 1000, id: 1}
  ) {
    portfolio {
      name
      portfolioId
    }
    errors {
      field
      messages
    }
  }
}
```

```
mutation UpdateWithError {
  updatePortfolio(input: {name: "New name", description: "New description"}) {
    portfolio {
      portfolioId
      name
      description
      initialAccountBalance
    }
    errors {
      field
      messages
    }
  }
}
```

```
mutation SellError {
 sellStock(input:{portfolio:1,stock:11, price:100, volume:100000})
  {
    trade{
      tradeId
      portfolio{name}
      stock{symbol}
      price
      volume
      tradeType
    }
    errors{
      field
      messages
    }
	}
}
```

```
mutation BuyError {
 buyStock(input:{portfolio:1,stock:11, price:10000000, volume:100000})
  {
    trade{
      tradeId
      portfolio{name}
      stock{symbol}
      price
      volume
      tradeType
    }
    errors{
      field
      messages
    }
	}
}
```
