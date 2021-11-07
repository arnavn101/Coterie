from authUser.models import CustomAccount
from interestsProfile.models import InterestProfile, AlgoIDToUserID
from interestsProfile.matching_algo import MatchingAlgo
from profileUser.interests_list import length


class InterestProfileManager:
    def __init__(self, user_object: CustomAccount):
        self.user_object = user_object
        self.user_interests_profile, _ = InterestProfile.objects.get_or_create(user_id=user_object)

    def initialize_interests(self, list_user_interests):
        success = True
        for individual_interest in list_user_interests:
            if individual_interest not in self.user_interests_profile.dict_interests_weights:
                success = False
                continue
            self.user_interests_profile.dict_interests_weights[individual_interest] = 1
        self.user_interests_profile.save(update_fields=['dict_interests_weights'])
        algo = MatchingAlgo(length)
        algo.add_vector_workflow(list(self.user_interests_profile.dict_interests_weights.values()))
        record = AlgoIDToUserID.objects.get_or_create()[0]
        record.mapping[algo.length()-1] = self.user_object.id
        record.save()
        return success

    def update_interests(self, new_list_interests):
        list_current_interests = set(self.user_interests_profile.dict_interests_weights.keys())
        new_interests = set(new_list_interests)
        to_reset = list(list_current_interests.difference(new_interests))
        success = True

        for individual_key in to_reset:
            self.user_interests_profile.dict_interests_weights[individual_key] = 0

        for individual_interest in new_list_interests:
            if individual_interest not in self.user_interests_profile.dict_interests_weights:
                success = False
                continue
            currentVal = self.user_interests_profile.dict_interests_weights[individual_interest]
            if currentVal == 0:
                self.user_interests_profile.dict_interests_weights[individual_interest] = 1
        self.user_interests_profile.save(update_fields=['dict_interests_weights'])
        self.rebuild_algo()
        return success

    def increase_interest(self, interest_input, increment_amt):
        self.user_interests_profile.dict_interests_weights[interest_input] += increment_amt
        self.user_interests_profile.save(update_fields=['dict_interests_weights'])
        self.rebuild_algo()

    def decrease_interest(self, interest_input, decrement_amt):
        self.user_interests_profile.dict_interests_weights[interest_input] -= decrement_amt
        self.user_interests_profile.save(update_fields=['dict_interests_weights'])
        self.rebuild_algo()

    def rebuild_algo(self):
        all_interest_profiles = InterestProfile.objects.all()
        algo = MatchingAlgo(length)
        record = AlgoIDToUserID.objects.get()
        record.mapping = {}
        for i_profile in all_interest_profiles:
            algo.add_vector(list(i_profile.dict_interests_weights.values()))
            record.mapping[algo.length()-1] = i_profile.id
        record.save()
        algo.serialize_index()
