"""
Check the calculation logic
"""

# Your data
rent = 3200
security = 5000
total_stated = 8200

print("=" * 60)
print("CALCULATION ANALYSIS")
print("=" * 60)

# Scenario 1: Total includes GST on rent
print("\nScenario 1: GST applied to rent")
print("-" * 60)
rent_with_gst = rent * 1.05
total_with_security = rent_with_gst + security
print(f"Rent: ₹{rent}")
print(f"Rent + GST (5%): ₹{rent_with_gst}")
print(f"Security: ₹{security}")
print(f"Total: ₹{total_with_security}")
print(f"Matches stated total ({total_stated})? {total_with_security == total_stated}")

# Scenario 2: Total does NOT include GST
print("\nScenario 2: NO GST (total = rent + security)")
print("-" * 60)
total_no_gst = rent + security
print(f"Rent: ₹{rent}")
print(f"Security: ₹{security}")
print(f"Total: ₹{total_no_gst}")
print(f"Matches stated total ({total_stated})? {total_no_gst == total_stated}")

# Scenario 3: GST already included in rent
print("\nScenario 3: Rent already includes GST")
print("-" * 60)
rent_before_gst = rent / 1.05
gst_amount = rent - rent_before_gst
total_with_security = rent + security
print(f"Rent (with GST): ₹{rent}")
print(f"Rent (before GST): ₹{rent_before_gst:.2f}")
print(f"GST amount: ₹{gst_amount:.2f}")
print(f"Security: ₹{security}")
print(f"Total: ₹{total_with_security}")
print(f"Matches stated total ({total_stated})? {total_with_security == total_stated}")

print("\n" + "=" * 60)
print("CONCLUSION:")
print("=" * 60)
if total_no_gst == total_stated:
    print("✅ Total = Rent + Security (NO GST added)")
    print("   The stated total does NOT include GST")
    print("   GST should be calculated and added separately")
elif total_with_security == total_stated:
    print("✅ Rent already includes GST")
    print("   The ₹3200 rent already has GST in it")
else:
    print("❓ Neither scenario matches exactly")
