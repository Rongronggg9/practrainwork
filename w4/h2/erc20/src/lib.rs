#![cfg_attr(not(feature = "std"), no_std)]

use liquid::storage;
use liquid_lang as liquid;
use liquid_primitives::types::Address;

#[liquid::contract]
mod erc20 {
    use super::*;

    type Balance = u128;

    /// Defines the state variables of your contract.
    #[liquid(storage)]
    struct Erc20 {
        pub total_supply: storage::Value<Balance>,
        balances: storage::Mapping<Address, Balance>,
        allowances: storage::Mapping<(Address, Address), Balance>,
    }

    #[liquid(event)]
    struct Transfer {
        #[liquid(indexed)]
        from: Address,
        #[liquid(indexed)]
        to: Address,
        value: u128,
    }

    #[liquid(event)]
    struct Approval {
        #[liquid(indexed)]
        owner: Address,
        #[liquid(indexed)]
        spender: Address,
        value: u128,
    }

    /// Defines the methods of your contract.
    #[liquid(methods)]
    impl Erc20 {
        /// Defines the constructor which will be executed automatically when the contract is
        /// under deploying. Usually constructor is used to initialize state variables.
        ///
        /// # Note
        /// 1. The name of constructor must be `new`;
        /// 2. The receiver of constructor must be `&mut self`;
        /// 3. The visibility of constructor must be `pub`.
        /// 4. The constructor should return nothing.
        /// 5. If you forget to initialize state variables, you
        ///    will be trapped in an runtime-error for attempting
        ///    to visit uninitialized storage.
        pub fn new(
            &mut self,
            initial_supply: Balance,
        ) {
            let caller = self.env().get_caller();
            self.total_supply.initialize(initial_supply);
            self.balances.initialize();
            self.balances.insert(caller, initial_supply);
            self.allowances.initialize();
        }

        pub fn balance_of(
            &self,
            owner: Address,
        ) -> Balance {
            let owner_argument = &owner;
            *self.balances.get(owner_argument).unwrap_or(&0)
        }

        pub fn transfer(
            &mut self,
            to: Address,
            value: Balance,
        ) -> bool {
            let from = self.env().get_caller();
            self.inner_transfer(from, to, value)
        }

        pub fn transfer_from(
            &mut self,
            from: Address,
            to: Address,
            value: Balance,
        ) -> bool {
            let caller = self.env().get_caller();
            let owner = &from;
            let spender = &caller;
            let allowance = *self
                .allowances
                .get(&(owner.clone(), spender.clone()))
                .unwrap_or(&0);
            if allowance < value {
                return false;
            }

            self.allowances
                .insert((from.clone(), caller.clone()), allowance - value);
            self.inner_transfer(from, to, value)
        }

        fn inner_transfer(
            &mut self,
            from: Address,
            to: Address,
            value: Balance,
        ) -> bool {
            let owner = &from;
            let from_balance = *self.balances.get(owner).unwrap_or(&0);
            if from_balance < value {
                return false;
            }

            self.balances.insert(from.clone(), from_balance - value);
            let owner = &to;
            let to_balance = *self.balances.get(owner).unwrap_or(&0);
            self.balances.insert(to.clone(), to_balance + value);
            self.env().emit(Transfer { from, to, value });
            true
        }

        pub fn approve(&mut self, spender: Address, value: Balance) -> bool {
            let owner = self.env().get_caller();
            self.allowances
                .insert((owner.clone(), spender.clone()), value);
            self.env().emit(Approval {
                owner,
                spender,
                value,
            });
            true
        }

        pub fn allowance(&self, owner: Address, spender: Address) -> Balance {
            let owner_argument = &owner;
            let spender_argument = &spender;
            *self
                .allowances
                .get(&(owner_argument.clone(), spender_argument.clone()))
                .unwrap_or(&0)
        }
    }

    /// Unit tests in Rust are normally defined within such a `#[cfg(test)]`
    /// module and test functions are marked with a `#[test]` attribute.
    /// The below code is technically just normal Rust code.
    #[cfg(test)]
    mod tests {
        /// Imports all the definitions from the outer scope so we can use them here.
        use super::*;
    }
}