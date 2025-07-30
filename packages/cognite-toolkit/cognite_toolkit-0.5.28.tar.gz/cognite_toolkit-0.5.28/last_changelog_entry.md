## cdf 

### Improved

- Standardization of authentication for Transformations, i.e., matching
`FunctionSchedules` and `WorkflowTrigger`. That is allow you to only
specify `clientId/clientSecret` if you are doing a transformation within
the same CDF Project as the Toolkit is configured for.
- Warning message if you set `sourceOidcCredentials` and
`destinationOidcCredentials`.

### Removed

- You can no longer set `sourceNonce` and `destinationNonce` directly in
a Transformation. You need to use
`authentication.clientId`/`authentication.ClientSecret` instead.

## templates

No changes.